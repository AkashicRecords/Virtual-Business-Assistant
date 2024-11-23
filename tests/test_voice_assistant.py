"""Tests for voice assistant functionality."""
import pytest
from gmail_assistant.voice_assistant import GmailVoiceAssistant
from unittest.mock import MagicMock, patch

@pytest.fixture
def assistant():
    with patch('speech_recognition.Recognizer'), \
         patch('pyttsx3.init'), \
         patch('gmail_assistant.voice_assistant.build'):
        return GmailVoiceAssistant()

def test_command_processing(assistant):
    """Test command processing"""
    assistant.read_latest_email = MagicMock()
    assert assistant.process_command("read email") == True
    assistant.read_latest_email.assert_called_once()

def test_invalid_command(assistant):
    """Test invalid command handling"""
    assistant.speak = MagicMock()
    assert assistant.process_command("invalid command") == False
    assistant.speak.assert_called_with("Command not recognized. Say 'help' for available commands.")

def test_listen_with_noise(assistant):
    """Test listening with background noise"""
    with patch('speech_recognition.Recognizer.recognize_google', side_effect=Exception("Could not understand audio")):
        assert assistant.listen() is None 