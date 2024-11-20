import unittest
from unittest.mock import Mock, patch
import speech_recognition as sr
from gmail_assistant.gmail_voice_assistant import GmailVoiceAssistant
from gmail_assistant.error_handler import GmailAssistantError

class TestGmailVoiceAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = GmailVoiceAssistant()
        
    @patch('speech_recognition.Recognizer.recognize_google')
    @patch('speech_recognition.Recognizer.listen')
    def test_listen_success(self, mock_listen, mock_recognize):
        # Arrange
        expected_text = "read email"
        mock_recognize.return_value = expected_text
        
        # Act
        result = self.assistant.listen()
        
        # Assert
        self.assertEqual(result, expected_text)
        mock_listen.assert_called_once()
        mock_recognize.assert_called_once()

    @patch('speech_recognition.Recognizer.recognize_google')
    @patch('speech_recognition.Recognizer.listen')
    def test_listen_unknown_value_error(self, mock_listen, mock_recognize):
        # Arrange
        mock_recognize.side_effect = sr.UnknownValueError()
        
        # Act & Assert
        with self.assertRaises(GmailAssistantError) as context:
            self.assistant.listen()
        self.assertIn("Could not understand audio", str(context.exception))

    @patch('speech_recognition.Recognizer.recognize_google')
    @patch('speech_recognition.Recognizer.listen')
    def test_listen_request_error(self, mock_listen, mock_recognize):
        # Arrange
        mock_recognize.side_effect = sr.RequestError("API unavailable")
        
        # Act & Assert
        with self.assertRaises(GmailAssistantError) as context:
            self.assistant.listen()
        self.assertIn("Could not request results", str(context.exception))

    @patch('pyttsx3.Engine.say')
    @patch('pyttsx3.Engine.runAndWait')
    def test_speak(self, mock_run_and_wait, mock_say):
        # Arrange
        test_text = "Hello, this is a test"
        
        # Act
        self.assistant.speak(test_text)
        
        # Assert
        mock_say.assert_called_once_with(test_text)
        mock_run_and_wait.assert_called_once()

    def test_setup_gmail_service(self):
        # This would test the Gmail service initialization
        # Would need to mock the OAuth credentials and service build
        pass

    def test_process_command(self):
        # This would test command processing
        # Would need to mock the command processor
        pass 