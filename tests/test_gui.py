"""Tests for the GUI module."""
import pytest
from gmail_assistant.gui import GmailAssistantGUI
import customtkinter as ctk

@pytest.fixture
def app():
    return GmailAssistantGUI()

def test_window_creation(app):
    """Test that the main window is created correctly"""
    assert isinstance(app.root, ctk.CTk)
    assert app.root.title() == "Gmail Voice Assistant"

def test_assistant_initialization(app):
    """Test that the voice assistant is initialized"""
    assert app.assistant is not None 