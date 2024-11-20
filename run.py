#!/usr/bin/env python3
import logging
from gmail_assistant.gmail_voice_assistant_gui import GmailVoiceAssistantGUI
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Start application
    app = GmailVoiceAssistantGUI()
    app.run()

if __name__ == "__main__":
    main() 