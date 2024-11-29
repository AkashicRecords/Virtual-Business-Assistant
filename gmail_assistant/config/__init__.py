"""Configuration package for Gmail Assistant."""
from .secrets import (
    GMAIL_CLIENT_ID,
    GMAIL_CLIENT_SECRET,
    GMAIL_REDIRECT_URI,
    SCOPES,
    TOKEN_PATH,
    CREDENTIALS_PATH
)

__all__ = [
    'GMAIL_CLIENT_ID',
    'GMAIL_CLIENT_SECRET',
    'GMAIL_REDIRECT_URI',
    'SCOPES',
    'TOKEN_PATH',
    'CREDENTIALS_PATH'
] 