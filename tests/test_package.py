import pytest
from gmail_assistant import GmailVoiceAssistant

def test_package_imports():
    """Test that the package can be imported correctly"""
    assert hasattr(GmailVoiceAssistant, '__init__') 