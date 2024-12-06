import speech_recognition as sr
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os.path
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize  
from nltk.tag import pos_tag  # Add this importt
from nltk.corpus import stopwords
import base64
from email.mime.text import MIMEText
import pyttsx3
from gmail_assistant.config.secrets import GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_REDIRECT_URI
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Gmail API setup
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Initialize TTS engine
engine = pyttsx3.init()

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                {
                    'installed': {
                        'client_id': GMAIL_CLIENT_ID,
                        'client_secret': GMAIL_CLIENT_SECRET,
                        'redirect_uris': [GMAIL_REDIRECT_URI],
                        'auth_uri': 'https://accounts.googlehttps://www.thaifriendly.com/Xxbeauty57.com/o/oauth2/auth',
                        'token_uri': 'https://oauth2.googleapis.com/token'
                    }
                },
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"Recognized command: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError:
        print("Sorry, there was an error with the speech recognition service.")
        return None

def process_command(command):
    tokens = word_tokenize(command.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    if 'read' in filtered_tokens and 'email' in filtered_tokens:
        return read_latest_email()
    elif 'send' in filtered_tokens and 'email' in filtered_tokens:
        return send_email()
    else:
        return "I'm sorry, I don't understand that command."

def read_latest_email():
    results = gmail_service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        return "You have no new emails."
    else:
        message = gmail_service.users().messages().get(userId='me', id=messages[0]['id']).execute()
        payload = message['payload']
        headers = payload['headers']

        subject = next(header['value'] for header in headers if header['name'] == 'Subject')
        sender = next(header['value'] for header in headers if header['name'] == 'From')

        if 'parts' in payload:
            body = payload['parts'][0]['body']['data']
        else:
            body = payload['body']['data']

        body = base64.urlsafe_b64decode(body).decode('utf-8')

        return f"Latest email from {sender}\nSubject: {subject}\n\n{body[:100]}..."

def send_email():
    recipient = input("To whom would you like to send the email? ")
    subject = input("What's the subject of the email? ")
    body = input("What's the content of the email? ")

    message = MIMEText(body)
    message['to'] = recipient
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    try:
        sent_message = gmail_service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        return f"Email sent successfully. Message Id: {sent_message['id']}"
    except Exception as e:
        return f"An error occurred: {e}"
    
def test_nltk_components(self):
    """Test NLTK components and data availability."""
    logger.info("Testing NLTK components...")
    try:
        # Download all required NLTK data first
        nltk.download('punkt', quiet=True)  # Changed from punkt_tab to punkt
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('maxent_ne_chunker', quiet=True)
        nltk.download('words', quiet=True)
        nltk.download('stopwords', quiet=True)  # Added stopwords download
        
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

def test_nlu_processing(self):
    """Test NLU processing capabilities."""
    logger.info("Testing NLU processing...")
    try:
        # Download ALL required NLTK data first - this is likely the root cause
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('tagsets', quiet=True)
        nltk.download('universal_tagset', quiet=True)
        
        # Test command
        command = "read latest email"
        tokens = word_tokenize(command)
        pos_tags = pos_tag(tokens)
        
        # Add this debug print to see what's actually happening
        logger.info(f"POS tags for '{command}': {pos_tags}")
        
        # Define valid command verbs (both base and inflected forms)
        valid_command_verbs = {
            'read', 'reads', 'reading',
            'send', 'sends', 'sending',
            'check', 'checks', 'checking',
            'show', 'shows', 'showing',
            'display', 'displays', 'displaying',
            'write', 'writes', 'writing'
        }
        
        # First check if word is in our valid verbs list (case-insensitive)
        # Then check if it's tagged as any form of verb by NLTK
        valid_command = any(
            word.lower() in valid_command_verbs or 
            tag.startswith('VB') or
            tag == 'MD'  # Modal verbs
            for word, tag in pos_tags
        )
                
        if not valid_command:
            logger.warning(f"Command: '{command}'")
            logger.warning(f"Tokens: {tokens}")
            logger.warning(f"POS tags: {pos_tags}")
            raise GmailAssistantError(f"No valid command verb found in: {command}")
            
        logger.info("NLU processing test successful")
        return True
        
    except Exception as e:
        error_msg = f"NLU processing test failed: {str(e)}"
        logger.error(error_msg)
        raise GmailAssistantError(error_msg)

def main():
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    
    global gmail_service
    gmail_service = authenticate_gmail()
    
    speak("Gmail voice assistant is ready. How can I help you?")
    
    while True:
        command = listen_for_command()
        if command:
            response = process_command(command)
            speak(response)
        
        if command and command.lower() in ['exit', 'quit']:
            speak("Goodbye!")
            break

if __name__ == '__main__':
    main()
