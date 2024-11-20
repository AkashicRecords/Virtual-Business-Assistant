import pytest
import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Test fixtures can be added here
@pytest.fixture
def mock_credentials():
    return {
        "token": "test_token",
        "refresh_token": "test_refresh_token",
        "client_id": "test_client_id",
        "client_secret": "test_client_secret"
    } 