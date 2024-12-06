# Virtual Business Assistant

A voice-controlled Gmail assistant that helps manage your email through natural language commands and LLM-enhanced processing.

## Table of Contents

### 📚 Documentation
- [API Documentation](docs/API.md)
- [Testing Standards](docs/testing_standards.md)
- [Test Plan](docs/test_plan.md)
- [Upcoming Features](docs/upcoming_features.md)
- [Changes Log](docs/CHANGES.md)

### 🚀 Features
- 🎤 Voice command interface for Gmail
- 🧠 Natural Language Processing
- 📧 Email operations:
  - Read emails with header extraction
  - Send emails with LLM assistance
  - Smart search functionality
  - Delete/archive management
  - Unread and important email filtering
- 🖥️ Modern GUI interface with real-time feedback
- 🤖 LLM integration for enhanced email processing
- 🔒 Secure OAuth2 authentication
- 📱 Cross-platform support (Windows, macOS, Linux)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AkashicRecords/Virtual-Business-Assistant.git
cd Virtual-Business-Assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. For development:
```bash
pip install -r requirements-dev.txt
```

## Quick Start

1. Configure Gmail API credentials (see [Configuration Guide](docs/configuration.md))
2. Run the assistant:
```bash
python -m gmail_assistant
```

## Configuration

### Gmail API Setup
1. Create a project in Google Cloud Console
2. Enable Gmail API
3. Configure OAuth2 consent screen
4. Create credentials (OAuth 2.0 Client ID)
5. Download credentials.json
6. Place in project root directory

### LLM Setup
- Default: Uses local Llama model
- Install and start Ollama
- Model path configuration in config.py
