import unittest
from unittest.mock import Mock, patch
from gmail_assistant.gmail_voice_assistant import GmailVoiceAssistant
from gmail_assistant.gmail_voice_assistant_gui import GmailVoiceAssistantGUI

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.gui = GmailVoiceAssistantGUI()
        self.assistant = self.gui.assistant

    def tearDown(self):
        self.gui.window.destroy()

    @patch('gmail_assistant.gmail_voice_assistant.GmailVoiceAssistant.listen')
    @patch('gmail_assistant.gmail_voice_assistant.GmailVoiceAssistant.process_command')
    def test_voice_command_flow(self, mock_process, mock_listen):
        """Test complete flow from voice command to GUI update"""
        # Arrange
        mock_listen.return_value = "read email"
        mock_process.return_value = "Reading your latest email..."
        
        # Act
        self.gui.toggle_listening()
        
        # Let the listen thread process
        self.gui.window.after(100, self.gui.window.quit)
        self.gui.window.mainloop()
        
        # Assert
        mock_listen.assert_called()
        mock_process.assert_called_with("read email")
        output_text = self.gui.output_text.get("1.0", "end-1c")
        self.assertIn("Reading your latest email...", output_text)

    @patch('gmail_assistant.gmail_voice_assistant.GmailVoiceAssistant.setup_gmail_service')
    def test_gmail_integration(self, mock_setup):
        """Test Gmail service integration"""
        # Arrange
        mock_service = Mock()
        mock_setup.return_value = mock_service
        
        # Act
        self.assistant.setup_gmail_service()
        
        # Assert
        mock_setup.assert_called_once()
        self.assertIsNotNone(self.assistant.gmail_service) 