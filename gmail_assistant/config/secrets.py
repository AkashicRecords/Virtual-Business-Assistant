import os
from dotenv import load_dotenv

load_dotenv()

GMAIL_CLIENT_ID = os.getenv('GMAIL_CLIENT_ID')
GMAIL_CLIENT_SECRET = os.getenv('GMAIL_CLIENT_SECRET')
GMAIL_REDIRECT_URI = os.getenv('GMAIL_REDIRECT_URI')

if not all([GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_REDIRECT_URI]):
    raise ValueError("Missing required environment variables. Please check your .env file.")
 