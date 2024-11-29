"""Handle Gmail OAuth2 authentication."""
import os
import pickle
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from .config.secrets import GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_REDIRECT_URI
from .error_handler import handle_errors

class AuthHandler:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
        self.token_path = os.path.join(os.path.dirname(__file__), 'resources', 'token.pickle')
        self.credentials_path = os.path.join(os.path.dirname(__file__), 'resources', 'credentials.json')
        
        # Create credentials.json if it doesn't exist
        if not os.path.exists(self.credentials_path):
            self.credentials = {
                'installed': {
                    'client_id': GMAIL_CLIENT_ID,
                    'client_secret': GMAIL_CLIENT_SECRET,
                    'redirect_uris': [GMAIL_REDIRECT_URI],
                    'auth_uri': "https://accounts.google.com/o/oauth2/auth",
                    'token_uri': "https://oauth2.googleapis.com/token"
                }
            }
            
            # Ensure the resources directory exists
            os.makedirs(os.path.dirname(self.credentials_path), exist_ok=True)
            
            # Write credentials to file
            with open(self.credentials_path, 'w') as f:
                json.dump(self.credentials, f)

    @handle_errors
    def get_credentials(self):
        """Get valid user credentials from storage.

        Returns:
            Credentials, the obtained credential.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.token_path), exist_ok=True)
            
            # Save the credentials for the next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        return creds 