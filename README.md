# Gmail Voice Assistant 🎤

A voice-controlled Gmail client with a modern GUI interface that allows you to manage your Gmail using voice commands.

## Prerequisites

- Python 3.8 or higher
- A Google Cloud Platform account
- Gmail account
- macOS or Windows

## Current Features

- Voice-controlled email management
- Modern GUI interface
- Email composition window
- Real-time voice recognition
- Basic email commands (read, send, delete)
- Command history display
- Status indicators

## Future Development
For detailed information about upcoming features, planned integrations, and future development roadmap, see our [Upcoming Features](docs/upcoming_features.md) document.

## Installation

### 1. Clone and Setup
```bash
# Clone the repository
git clone [repository-url]
cd gmail-voice-assistant

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install the package
pip install -e .
```

### 2. Google API Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop Application"
   - Download the credentials JSON file
   - Save as `gmail_assistant/resources/credentials.json`

### 3. Run the Application
```bash
gmail-assistant
```

On first run:
1. A browser window will open for Gmail authentication
2. Sign in with your Google account
3. Grant the requested permissions
4. The application window will appear

## Usage

### Voice Commands
- "Read email" - Reads your latest email
- "Send email" - Opens email composition window
- "Check inbox" - Lists recent emails
- "Delete email" - Deletes the latest email
- "Mark as read" - Marks latest email as read
- "Help" - Lists all available commands

### GUI Features
- Start/Stop listening button
- Command output display
- Email composition window
- Status indicators

## Development

For development setup and contribution guidelines, see [Developer Documentation](docs/developer.md)

## Upcoming Features

For information about upcoming features, development plans, and technical architecture, see our [Development Plans](docs/upcoming_features.md)

## Troubleshooting

### Common Issues
1. **Microphone not working**
   - Check system microphone permissions
   - Verify microphone is selected as input device

2. **Authentication Issues**
   - Ensure credentials.json is in the correct location
   - Check Google Cloud Console for API enablement
   - Delete token.pickle to re-authenticate

3. **Installation Issues**
   - Make sure all dependencies are installed
   - Check Python version compatibility
   - Verify virtual environment activation

## License

[Your License Here]