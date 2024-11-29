# Gmail Voice Assistant 🎤

A voice-controlled Gmail client with LLM integration that allows you to manage your Gmail using voice commands and AI assistance.

## Architecture

The application is built using a microservices architecture:

### Services
- **Voice Service**: Handles speech-to-text and voice commands
- **LLM Service**: Manages AI/LLM interactions using local Ollama
- **Gmail Service**: Handles Gmail API interactions

### Core Components
- Modern GUI with CustomTkinter
- Real-time voice processing
- Local LLM integration with Ollama
- Gmail API integration

## Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account
- Gmail account
- Ollama with Llama2 model installed
- macOS or Windows

## Quick Start

1. **Install Dependencies**:
```bash
pip install -e .
```

2. **Configure Services**:
- Set up Google Cloud credentials
- Install and start Ollama
- Configure environment variables

3. **Run the Application**:
```bash
gmail-assistant
```

## Features

### Voice Commands
- Email management (read, send, delete)
- Smart search and filtering
- Context-aware responses

### AI Features
- Smart email composition
- Content improvement suggestions
- Context understanding
- Natural language processing

### Gmail Integration
- Full Gmail API support
- Real-time email monitoring
- Thread management

## Development

### Service Development
```bash
# Start individual services
python -m gmail_assistant.services.voice.api
python -m gmail_assistant.services.llm.api
python -m gmail_assistant.services.gmail.api
```

### Testing
```bash
pytest tests/
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

[Your License]

## Installation

### Prerequisites

- Python 3.8 or higher
- pip
- virtualenv (recommended)

### Quick Install
```bash
# Create and activate virtual