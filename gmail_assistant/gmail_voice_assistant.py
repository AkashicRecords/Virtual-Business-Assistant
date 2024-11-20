import speech_recognition as sr
import pyttsx3
from .auth_handler import AuthHandler
from .command_processor import CommandProcessor
from .error_handler import handle_errors, GmailAssistantError
from googleapiclient.discovery import build
import logging

logger = logging.getLogger(__name__)

class GmailVoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.auth_handler = AuthHandler()
        self.command_processor = CommandProcessor()
        self.gmail_service = None
        self.setup_gmail_service()

    @handle_errors
    def setup_gmail_service(self):
        """Initialize Gmail service with OAuth credentials."""
        creds = self.auth_handler.get_credentials()
        self.gmail_service = build('gmail', 'v1', credentials=creds)

    @handle_errors
    def listen(self):
        """Listen for voice input and return recognized text."""
        with sr.Microphone() as source:
            logger.info("Listening for command...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            
        try:
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            raise GmailAssistantError("Could not understand audio")
        except sr.RequestError as e:
            raise GmailAssistantError(f"Could not request results: {str(e)}")

    def speak(self, text):
        """Convert text to speech."""
        logger.info(f"Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def process_command(self, command_text):
        """Process the recognized command."""
        return self.command_processor.process_command(command_text)

    def run(self):
        """Main loop for voice assistant."""
        self.speak("Gmail voice assistant is ready")
        while True:
            try:
                command_text = self.listen()
                if command_text:
                    response = self.process_command(command_text)
                    self.speak(response)
            except GmailAssistantError as e:
                logger.error(f"Error: {str(e)}")
                self.speak(f"Sorry, there was an error: {str(e)}") 