import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GMAIL_CLIENT_ID = os.getenv('GMAIL_CLIENT_ID')
    GMAIL_CLIENT_SECRET = os.getenv('GMAIL_CLIENT_SECRET')
    GMAIL_REDIRECT_URI = os.getenv('GMAIL_REDIRECT_URI')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        required_vars = [
            'GMAIL_CLIENT_ID',
            'GMAIL_CLIENT_SECRET',
            'GMAIL_REDIRECT_URI'
        ]
        
        missing = [var for var in required_vars if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}") 