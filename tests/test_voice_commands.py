import pytest
from unittest.mock import MagicMock, patch
from gmail_assistant.voice_assistant import GmailVoiceAssistant

@pytest.fixture
def mock_assistant():
    with patch('speech_recognition.Recognizer'), \
         patch('pyttsx3.init'), \
         patch('gmail_assistant.voice_assistant.build'):
        assistant = GmailVoiceAssistant()
        assistant.service = MagicMock()
        return assistant

class TestBasicVoiceCommands:
    def test_read_latest_email(self, mock_assistant):
        # Mock email data
        mock_email = {
            'messages': [{
                'id': '123',
                'payload': {
                    'headers': [{'name': 'Subject', 'value': 'Test Email'}]
                }
            }]
        }
        mock_assistant.service.users().messages().list().execute.return_value = mock_email
        mock_assistant.service.users().messages().get().execute.return_value = mock_email['messages'][0]
        
        # Test command
        mock_assistant.process_command("read email")
        mock_assistant.speak.assert_called_with("Latest email subject: Test Email") 