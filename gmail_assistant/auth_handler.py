"""Handle Gmail OAuth2 authentication."""
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class AuthHandler:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
        self.token_path = 'token.pickle'
        self.credentials_path = 'credentials.json'

    def get_credentials(self):
        creds = None
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        return creds 