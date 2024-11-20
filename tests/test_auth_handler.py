import unittest
from unittest.mock import Mock, patch
from gmail_assistant.auth_handler import AuthHandler
from google.auth.exceptions import RefreshError

class TestAuthHandler(unittest.TestCase):
    def setUp(self):
        self.auth_handler = AuthHandler()

    @patch('google.oauth2.credentials.Credentials.from_authorized_user_file')
    def test_load_existing_credentials(self, mock_creds):
        """Test loading existing credentials"""
        # Arrange
        mock_creds.return_value.valid = True
        
        # Act
        creds = self.auth_handler.get_credentials()
        
        # Assert
        self.assertIsNotNone(creds)
        mock_creds.assert_called_once()

    @patch('google.oauth2.credentials.Credentials.from_authorized_user_file')
    def test_refresh_expired_credentials(self, mock_creds):
        """Test refreshing expired credentials"""
        # Arrange
        mock_creds.return_value.valid = False
        mock_creds.return_value.expired = True
        mock_creds.return_value.refresh_token = "test_refresh_token"
        
        # Act
        creds = self.auth_handler.get_credentials()
        
        # Assert
        self.assertIsNotNone(creds)
        mock_creds.return_value.refresh.assert_called_once()

    @patch('google.oauth2.credentials.Credentials.from_authorized_user_file')
    def test_handle_refresh_error(self, mock_creds):
        """Test handling credential refresh error"""
        # Arrange
        mock_creds.return_value.valid = False
        mock_creds.return_value.expired = True
        mock_creds.return_value.refresh.side_effect = RefreshError()
        
        # Act & Assert
        with self.assertRaises(Exception):
            self.auth_handler.get_credentials() 