import speech_recognition as sr
import pyttsx3
from .auth_handler import AuthHandler
from .command_processor import CommandProcessor
from .error_handler import handle_errors, GmailAssistantError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from .llm_service import LLMService

logger = logging.getLogger(__name__)

class GmailVoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.auth_handler = AuthHandler()
        self.command_processor = CommandProcessor()
        self.gmail_service = None
        self.llm_service = LLMService()
        
        # Initialize and test all components
        logger.info("Initializing Gmail Voice Assistant...")
        self.test_nltk_components()
        self.setup_gmail_service()
        self.test_api_endpoints()
        self.test_voice_components()
        self.test_nlu_processing()
        logger.info("Initialization complete!")

    def test_nltk_components(self):
        """Test NLTK components and data availability."""
        logger.info("Testing NLTK components...")
        try:
            # Download all required NLTK data first
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('maxent_ne_chunker', quiet=True)
            nltk.download('words', quiet=True)
            nltk.download('stopwords', quiet=True)
            
            # Test text
            test_text = "Test email processing capabilities."
            
            # Test sentence tokenization first
            sentences = sent_tokenize(test_text)
            
            # Then test word tokenization
            for sentence in sentences:
                tokens = word_tokenize(sentence)
                pos_tags = pos_tag(tokens)
            
            logger.info("NLTK components test successful")
            return True
            
        except Exception as e:
            error_msg = f"NLTK components test failed: {str(e)}"
            logger.error(error_msg)
            raise GmailAssistantError(error_msg)

    def test_voice_components(self):
        """Test voice recognition and synthesis components."""
        logger.info("Testing voice components...")
        try:
            # Test text-to-speech
            self.engine.getProperty('voices')  # Test engine initialization
            
            # Test speech recognition initialization
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            logger.info("Voice components test successful")
            return True
        except Exception as e:
            error_msg = f"Voice components test failed: {str(e)}"
            logger.error(error_msg)
            raise GmailAssistantError(error_msg)

    def test_nlu_processing(self):
        """Test NLU processing capabilities."""
        logger.info("Testing NLU processing...")
        try:
            # Test command
            command = "read latest email"
            tokens = word_tokenize(command)
            pos_tags = pos_tag(tokens)
            
            # Add debug logging
            logger.debug(f"POS tags for '{command}': {pos_tags}")
            
            # Define valid command verbs (both base and inflected forms)
            valid_command_verbs = {
                'read', 'reads', 'reading',
                'send', 'sends', 'sending',
                'check', 'checks', 'checking',
                'show', 'shows', 'showing',
                'display', 'displays', 'displaying',
                'write', 'writes', 'writing'
            }
            
            # Check for valid commands - FIXED: Check the actual word, not just splitting
            command_verbs = []
            for word, tag in pos_tags:
                word = word.lower()
                if tag.startswith('VB') or word in valid_command_verbs:
                    command_verbs.append(word)
                    
            valid_command = any(verb in valid_command_verbs for verb in command_verbs)
                    
            if not valid_command:
                logger.warning(f"Command: '{command}'")
                logger.warning(f"Tokens: {tokens}")
                logger.warning(f"POS tags: {pos_tags}")
                logger.warning(f"Identified verbs: {command_verbs}")
                raise GmailAssistantError(f"No valid command verb found in: {command}")
                
            logger.info("NLU processing test successful")
            return True
            
        except Exception as e:
            error_msg = f"NLU processing test failed: {str(e)}"
            logger.error(error_msg)
            raise GmailAssistantError(error_msg)

    @handle_errors
    def setup_gmail_service(self):
        """Initialize Gmail service with OAuth credentials."""
        creds = self.auth_handler.get_credentials()
        self.gmail_service = build('gmail', 'v1', credentials=creds)
        self.command_processor.set_gmail_service(self.gmail_service)

    @handle_errors
    def test_api_endpoints(self):
        """Test Gmail API endpoints to ensure they're working."""
        logger.info("Testing Gmail API endpoints...")
        
        try:
            # Test 1: Profile access
            logger.info("Testing profile access...")
            profile = self.gmail_service.users().getProfile(userId='me').execute()
            logger.info(f"Profile access successful. Email: {profile['emailAddress']}")

            # Test 2: Labels access
            logger.info("Testing labels access...")
            labels = self.gmail_service.users().labels().list(userId='me').execute()
            logger.info(f"Labels access successful. Found {len(labels.get('labels', []))} labels")

            # Test 3: Messages access
            logger.info("Testing messages access...")
            messages = self.gmail_service.users().messages().list(
                userId='me', maxResults=1).execute()
            if messages.get('messages', []):
                logger.info("Messages access successful")
            else:
                logger.info("Messages access successful (no messages found)")

            # Test 4: Draft access
            logger.info("Testing drafts access...")
            drafts = self.gmail_service.users().drafts().list(userId='me').execute()
            logger.info("Drafts access successful")

            logger.info("All API endpoint tests completed successfully!")
            return True

        except HttpError as error:
            error_message = f"API endpoint test failed: {str(error)}"
            logger.error(error_message)
            raise GmailAssistantError(error_message)

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
        # First try to identify if it's a specific email command
        for cmd in self.command_processor.commands:
            if cmd in command_text.lower():
                return self.command_processor.process_command(command_text)
        
        # If not a specific command, treat as conversation
        return self.llm_service.process_conversation(command_text)

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