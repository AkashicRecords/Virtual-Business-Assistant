# Gmail Voice Assistant 🎤

A Python-based voice-controlled Gmail client that allows users to manage their emails using voice commands and a modern GUI interface. The application combines speech recognition, Gmail API integration, and a CustomTkinter interface for an accessible email management experience.

## ✨ Features

- **Voice Control**: 
  - Speech recognition for email commands
  - Text-to-speech responses
  - Continuous listening mode
  
- **Email Operations**:
  - Read latest emails
  - Send new emails
  - Basic email management
  
- **Modern GUI**:
  - Clean CustomTkinter interface
  - Real-time status updates
  - Email composition window
  - Command output display

## 🔧 Technical Components

### Core Modules
- `gmail_voice_assistant.py`: Core voice assistant functionality
- `gmail_voice_assistant_gui.py`: GUI implementation
- `run.py`: Application entry point

### Dependencies
- **Speech Processing**:
  - `speech_recognition`
  - `pyttsx3`
  - `PyAudio`
  
- **Gmail Integration**:
  - `google-auth-oauthlib`
  - `google-api-python-client`
  
- **GUI**:
  - `customtkinter`
  - `pillow`
  
- **Natural Language Processing**:
  - `nltk`

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.8 or higher
- A Google Cloud Platform account
- A Gmail account
- Git
- System audio requirements:
  - Linux: `portaudio19-dev` and `python3-pyaudio`
  - Windows: No additional requirements
  - macOS: `portaudio` via Homebrew

### 2. Google Cloud Platform Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"
4. Configure OAuth Consent Screen:
   - Go to "APIs & Services" > "OAuth consent screen"
   - Choose "External" user type
   - Fill in required application information
   - Add necessary scopes for Gmail API
5. Create Credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop Application"
   - Download the credentials JSON file
   - Rename it to `credentials.json`

### 3. Project Setup

1. **Clone the Repository**
   ```bash
   git clone [repository-url]
   cd gmail-voice-assistant
   ```

2. **System Dependencies (Linux Only)**
   ```bash
   sudo apt-get update
   sudo apt-get install portaudio19-dev python3-pyaudio
   ```

3. **Create Virtual Environment**
   ```bash
   # Using setup script
   chmod +x setup.sh
   ./setup.sh
   
   # Or manually
   python -m venv venv
   source venv/bin/activate  # Windows: .\venv\Scripts\activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Gmail API**
   - Place the downloaded `credentials.json` in the project root directory
   - First run will prompt OAuth2 authentication in browser
   - Token will be saved as `token.json`

### 4. Environment Configuration

1. Create `.env` file in project root:
   ```
   GMAIL_CLIENT_ID=your_client_id_from_credentials
   GMAIL_CLIENT_SECRET=your_client_secret_from_credentials
   GMAIL_REDIRECT_URI=http://localhost
   ```

2. Install NLTK Data:
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

### 5. Verify Installation

1. **Test the Setup**
   ```bash
   python run.py
   ```

2. **First Run**
   - Application will open browser for Gmail authentication
   - Grant necessary permissions
   - Verify GUI window appears
   - Test microphone access

### 6. Docker Setup (Optional)

#### Windows Setup

1. **Install Docker Desktop**
   - Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
   - Install and follow setup wizard
   - Ensure WSL 2 is installed if prompted
   - Restart your computer if required

2. **Configure Docker**
   ```powershell
   # Open PowerShell as Administrator
   
   # Create project directory if not exists
   mkdir C:\gmail-voice-assistant
   cd C:\gmail-voice-assistant
   
   # Copy your project files and credentials here
   copy credentials.json C:\gmail-voice-assistant\
   ```

3. **Build and Run**
   ```powershell
   # Build the image
   docker build -t gmail-voice-assistant .
   
   # Run with Windows audio passthrough
   docker run -v ${PWD}/tokens:/app/tokens `
             --device="/dev/snd:/dev/snd" `
             -e DISPLAY=${Env:DISPLAY} `
             --name gmail-assistant `
             gmail-voice-assistant
   ```

#### macOS Setup

1. **Install Docker Desktop**
   - Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
   - Install the application
   - Start Docker Desktop and wait for it to initialize

2. **Install Audio Dependencies**
   ```bash
   # Using Homebrew
   brew install pulseaudio
   
   # Start PulseAudio server
   pulseaudio --load=module-native-protocol-tcp --exit-idle-time=-1 --daemon
   ```

3. **Configure Project**
   ```bash
   # Create project directory
   mkdir ~/gmail-voice-assistant
   cd ~/gmail-voice-assistant
   
   # Copy your project files and credentials
   cp /path/to/credentials.json .
   ```

4. **Build and Run**
   ```bash
   # Build the image
   docker build -t gmail-voice-assistant .
   
   # Run with macOS audio passthrough
   docker run -v $(pwd)/tokens:/app/tokens \
             -v ~/.config/pulse:/root/.config/pulse \
             -e PULSE_SERVER=docker.for.mac.localhost \
             --name gmail-assistant \
             gmail-voice-assistant
   ```

#### Docker Troubleshooting

1. **Windows Issues**
   - Ensure Docker Desktop is running with WSL 2 backend
   - Check Windows audio settings
   - Try running Docker commands in PowerShell as Administrator
   ```powershell
   # Reset Docker Desktop
   wsl --shutdown
   net stop com.docker.service
   net start com.docker.service
   ```

2. **macOS Issues**
   - Verify PulseAudio is running
   ```bash
   # Check PulseAudio status
   pulseaudio --check
   
   # Restart PulseAudio if needed
   pulseaudio -k
   pulseaudio --start
   ```

3. **General Docker Issues**
   ```bash
   # Remove existing container
   docker rm -f gmail-assistant
   
   # Clean up Docker system
   docker system prune
   
   # Check Docker logs
   docker logs gmail-assistant
   ```

4. **Audio Device Issues**
   - Windows: Check Device Manager for audio devices
   - macOS: Verify audio permissions in System Preferences
   - Test audio outside Docker first
   ```bash
   # Test microphone
   python -m sounddevice
   ```

### Troubleshooting Common Issues

1. **Audio Issues**
   - Check microphone permissions
   - Verify PyAudio installation
   - Test system audio input

2. **Gmail API Issues**
   - Verify credentials.json is present
   - Check OAuth consent screen configuration
   - Ensure correct API scopes

3. **Dependencies Issues**
   - Update pip: `pip install --upgrade pip`
   - Install wheel: `pip install wheel`
   - Try installing requirements individually

## 🎯 Usage

### Running the Application

```bash
# Using run.py
python run.py

# Or using entry point
gmail-assistant
```

### Voice Commands
- "Read email" - Reads the latest email
- "Send email" - Opens email composition window
- More commands can be added through the command processor

### GUI Features
- Start/Stop listening button
- Email composition window
- Status indicators
- Command output display

## 🐳 Docker Support

```bash
# Build the image
docker build -t gmail-voice-assistant .

# Run the container
docker run -v $(pwd)/tokens:/app/tokens gmail-voice-assistant
```

## 📁 Project Structure

```
gmail-voice-assistant/
├── gmail_assistant/
│   ├── __init__.py
│   ├── gmail_voice_assistant.py     # Core voice assistant functionality
│   ├── gmail_voice_assistant_gui.py # GUI implementation
│   ├── auth_handler.py             # Gmail authentication handling
│   ├── command_processor.py        # Voice command processing
│   └── error_handler.py           # Error handling utilities
├── tests/
│   └── test_gmail_assistant.py
├── .env                           # Environment variables
├── .gitignore
├── Dockerfile                     # Docker configuration
├── LICENSE
├── README.md
├── requirements.txt              # Project dependencies
├── run.py                       # Application entry point
├── setup.py                     # Package setup configuration
└── setup.sh                     # Setup script
```

### Key Components

1. **Core Modules**
   - `gmail_voice_assistant.py`: Handles speech recognition, TTS, and Gmail operations
   - `gmail_voice_assistant_gui.py`: CustomTkinter-based GUI implementation
   - `auth_handler.py`: Manages Gmail API authentication
   - `command_processor.py`: Processes voice commands
   - `error_handler.py`: Error handling and logging

2. **Configuration Files**
   - `.env`: Environment variables configuration
   - `setup.py`: Package installation configuration
   - `requirements.txt`: Project dependencies
   - `Dockerfile`: Docker container configuration

3. **Scripts**
   - `run.py`: Main entry point
   - `setup.sh`: Environment setup script

## 🔑 Authentication

The application uses OAuth 2.0 for Gmail API authentication. On first run:
1. Browser opens for Gmail authentication
2. Grant necessary permissions
3. Credentials are saved as `token.json`

## 🎮 Controls

### GUI Elements
- Status indicator showing current state
- Start/Stop listening button
- Email composition window
- Command output display area

### Voice Commands
- "Read email" - Reads latest email
- "Send email" - Opens email composition window
- "Exit" or "Quit" - Closes the application

## 🛠️ Development

### Adding New Commands
1. Update `command_processor.py`
2. Add command handler in `gmail_voice_assistant.py`
3. Update GUI if needed in `gmail_voice_assistant_gui.py`

### Testing
```bash
python -m pytest tests/
```

### Building Docker Image
```bash
docker build -t gmail-voice-assistant .
```

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-mock pytest-cov

# Run all tests
python -m pytest tests/

# Run with coverage report
python -m pytest --cov=gmail_assistant tests/

# Run specific test category
python -m pytest tests/test_integration.py
```

### Test Categories
- **Unit Tests**
  - `test_gmail_voice_assistant.py`: Core functionality tests
  - `test_gmail_voice_assistant_gui.py`: GUI component tests
  - `test_command_processor.py`: Command processing tests
  - `test_auth_handler.py`: Authentication handling tests
  
- **Integration Tests**
  - `test_integration.py`: End-to-end workflow tests
  
- **Test Configuration**
  - `conftest.py`: Shared fixtures and configuration

### Test Coverage
To generate a detailed coverage report:
```bash
python -m pytest --cov=gmail_assistant --cov-report=html tests/
```
The report will be available in the `htmlcov` directory.

### GUI Testing with Selenium
```bash
# Install Selenium dependencies
pip install selenium webdriver-manager

# Run Selenium tests
python -m pytest tests/test_selenium_gui.py
```

#### Selenium Test Categories
- Initial window state and component presence
- Button interactions and state changes
- Text output updates
- Email composition window functionality

#### Requirements
- Chrome browser installed
- ChromeDriver (automatically managed by webdriver-manager)
- X server for Linux systems running GUI tests

#### Headless Testing
Tests run in headless mode by default. To run with visible browser:
```python
chrome_options.remove_argument('--headless')
```
