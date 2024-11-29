"""Core voice assistant functionality."""
import speech_recognition as sr
import pyttsx3
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
import json
from .utils import handle_errors
from .config.secrets import SCOPES, CREDENTIALS_PATH, TOKEN_PATH
from .llm.service import LLMService
from .voice_processing.service import VoiceProcessor
from datetime import datetime
from .utils.logger import logger

class GmailVoiceAssistant:
    @handle_errors
    def __init__(self):
        logger.info("Initializing Gmail Voice Assistant")
        try:
            self.recognizer = sr.Recognizer()
            self.engine = pyttsx3.init()
            self.credentials = None
            self.service = None
            
            logger.info("Setting up Gmail API...")
            self.setup_gmail_api()
            
            logger.info("Initializing LLM service...")
            self.llm_service = LLMService()
            
            logger.info("Initializing voice processor...")
            self.voice_processor = VoiceProcessor()
            
            logger.info("Setting up commands...")
            self.commands = {
                "read email": self.read_latest_email,
                "send email": self.compose_email,
                "check inbox": self.check_inbox,
                "delete email": self.delete_latest_email,
                "mark as read": self.mark_as_read,
                "help": self.list_commands
            }
            
            logger.info("Voice assistant initialization complete")
            
        except Exception as e:
            logger.error(f"Failed to initialize voice assistant: {str(e)}")
            raise

    @handle_errors
    def setup_gmail_api(self):
        logger.info("Setting up Gmail API")
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as token:
                self.credentials = pickle.load(token)

        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH, 
                    SCOPES
                )
                self.credentials = flow.run_local_server(port=8080)
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(self.credentials, token)

        self.service = build('gmail', 'v1', credentials=self.credentials)

    @handle_errors
    def listen(self):
        """Listen for voice commands"""
        logger.info("Listening for commands...")
        try:
            with sr.Microphone() as source:
                logger.debug("Microphone initialized")
                logger.debug("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Adjusted for ambient noise")
                
                self.speak("Listening...")
                logger.debug("Waiting for audio input...")
                
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    logger.info("Audio captured successfully")
                    
                    # Process the command
                    logger.debug("Processing captured audio...")
                    return self.process_command(audio)
                    
                except sr.WaitTimeoutError:
                    logger.warning("No audio input received (timeout)")
                    self.speak("I didn't hear anything. Please try again.")
                    return None
                except Exception as e:
                    logger.error(f"Error during audio capture: {str(e)}", exc_info=True)
                    self.speak("Sorry, there was an error. Please try again.")
                    return None
                
        except Exception as e:
            logger.error(f"Critical error in listen method: {str(e)}", exc_info=True)
            self.speak("Sorry, there was a problem with the microphone.")
            return None

    @handle_errors
    def speak(self, text):
        """Convert text to speech"""
        logger.info(f"Speaking: {text}")
        
        # Get current engine properties
        rate = self.engine.getProperty('rate')
        
        # Set the speaking rate to half the default speed
        # Default is usually around 200 words per minute
        self.engine.setProperty('rate', 100)  # Reduce to half speed
        
        self.engine.say(text)
        self.engine.runAndWait()

    @handle_errors
    def process_command(self, audio_data):
        """Process voice command"""
        try:
            # First try to get the text from the audio
            result = self.voice_processor.process_audio(audio_data)
            
            if not result:
                self.speak("I couldn't understand that. Please try again.")
                return False
            
            logger.info(f"Processing command: {result.text}")
            
            # Check for direct command matches first
            for command_phrase, command_func in self.commands.items():
                if command_phrase in result.text:
                    logger.info(f"Executing command: {command_phrase}")
                    command_func()
                    return True
            
            # If no direct match, use LLM analysis
            analysis = self.llm_service.analyze_query(result.text)
            logger.info(f"LLM analysis: {analysis}")
            
            if analysis['confidence'] > 0.7:
                return self.handle_command(analysis)
            
            self.speak("I'm not sure what you want me to do. Could you rephrase that?")
            return False
            
        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            self.speak("Sorry, there was an error processing your command.")
            return False

    def handle_command(self, analysis):
        """Handle analyzed command"""
        command_type = analysis['query_type']
        params = analysis['parameters']
        
        if command_type == "email_read":
            return self.read_latest_email()
        elif command_type == "email_send":
            return self.compose_email(params)
        elif command_type == "email_search":
            return self.search_emails(params)
        # ... handle other command types ...

    @handle_errors
    def read_latest_email(self):
        """Read the latest email"""
        results = self.service.users().messages().list(userId='me', maxResults=1).execute()
        if 'messages' in results:
            message = self.service.users().messages().get(userId='me', id=results['messages'][0]['id']).execute()
            subject = next(header['value'] for header in message['payload']['headers'] if header['name'] == 'Subject')
            self.speak(f"Latest email subject: {subject}")
        else:
            self.speak("No emails found")

    @handle_errors
    def send_email(self, to, subject, body):
        """Send an email"""
        logger.info(f"Sending email to: {to}")
        try:
            message = self._create_message(to, subject, body)
            self.service.users().messages().send(userId='me', body=message).execute()
            self.speak("Email sent successfully")
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            self.speak("Failed to send email")

    def _create_message(self, to, subject, body):
        """Create email message"""
        from email.mime.text import MIMEText
        from base64 import urlsafe_b64encode
        
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        raw = urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw}

    @handle_errors
    def check_inbox(self):
        """Check inbox for recent emails"""
        logger.info("Checking inbox")
        results = self.service.users().messages().list(userId='me', maxResults=5).execute()
        if 'messages' in results:
            self.speak("Recent emails:")
            for msg in results['messages']:
                message = self.service.users().messages().get(userId='me', id=msg['id']).execute()
                subject = next(header['value'] for header in message['payload']['headers'] if header['name'] == 'Subject')
                self.speak(subject)
        else:
            self.speak("No emails found")

    @handle_errors
    def delete_latest_email(self):
        """Delete the latest email"""
        logger.info("Deleting latest email")
        results = self.service.users().messages().list(userId='me', maxResults=1).execute()
        if 'messages' in results:
            msg_id = results['messages'][0]['id']
            self.service.users().messages().trash(userId='me', id=msg_id).execute()
            self.speak("Email deleted")
        else:
            self.speak("No emails to delete")

    @handle_errors
    def mark_as_read(self):
        """Mark the latest email as read"""
        logger.info("Marking latest email as read")
        results = self.service.users().messages().list(userId='me', maxResults=1).execute()
        if 'messages' in results:
            msg_id = results['messages'][0]['id']
            self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            self.speak("Email marked as read")
        else:
            self.speak("No emails to mark as read")

    @handle_errors
    def compose_email(self):
        """Placeholder for email composition"""
        logger.info("Opening email composition window")
        self.speak("Please use the email composition window to write your message")
        # The actual composition is handled by the GUI

    @handle_errors
    def list_commands(self):
        """List available commands"""
        logger.info("Listing available commands")
        commands_list = ", ".join(self.commands.keys())
        self.speak(f"Available commands are: {commands_list}")