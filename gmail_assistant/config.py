"""Configuration settings for the application."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_DIR = os.path.join(os.path.dirname(__file__), 'resources')

# Gmail API settings
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
CREDENTIALS_PATH = os.path.join(RESOURCES_DIR, 'credentials.json')
TOKEN_PATH = os.path.join(RESOURCES_DIR, 'token.pickle')

# GUI settings
WINDOW_SIZE = "800x600"
DARK_MODE = True 

# Remove the explicit OAuth port config since Desktop app handles it
# OAUTH_PORT = 8080
# OAUTH_REDIRECT_URI = f"http://localhost:{OAUTH_PORT}"