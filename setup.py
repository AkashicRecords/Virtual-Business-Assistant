from setuptools import setup, find_packages
import platform
import subprocess
import sys

def install_system_dependencies():
    """Install system-level dependencies based on the platform."""
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        try:
            # Install llama-cpp-python with Metal support
            subprocess.run([
                "CMAKE_ARGS='-DLLAMA_METAL=on' pip install llama-cpp-python --no-cache-dir --force-reinstall"
            ], shell=True, check=True)
            
            # Check if Homebrew is installed
            subprocess.run(["brew", "--version"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("Homebrew is required. Please install it from https://brew.sh/")
            sys.exit(1)
            
        try:
            # Check if portaudio is installed
            result = subprocess.run(["brew", "list", "portaudio"], 
                                 check=False, capture_output=True, text=True)
            if result.returncode != 0:
                print("Installing portaudio...")
                subprocess.run(["brew", "install", "portaudio"], check=True)
            else:
                print("portaudio is already installed")
        except Exception as e:
            print(f"Error checking/installing portaudio: {e}")
            sys.exit(1)
        
    elif system == "linux":
        try:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", 
                          "python3-pyaudio", "portaudio19-dev"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing system dependencies: {e}")
            sys.exit(1)
        
    elif system == "windows":
        print("On Windows, PyAudio wheel will be installed automatically.")

def post_install():
    """Run post-installation tasks."""
    try:
        import nltk
        print("Downloading required NLTK data...")
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
    except ImportError:
        print("NLTK will be installed with other dependencies.")

# Run system dependency installation
if "install" in sys.argv:
    install_system_dependencies()

setup(
    name="gmail-voice-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Core dependencies
        "google-auth-oauthlib",
        "google-auth",
        "google-api-python-client",
        
        # Voice processing
        "SpeechRecognition",
        "pyaudio",
        "pyttsx3",
        
        # GUI
        "customtkinter",
        "pillow",  # For image handling in GUI
        
        # Networking and API
        "requests",
        
        # Utilities
        "python-dotenv",  # For environment variables
        "loguru",  # Better logging
        "nltk",    # Natural Language Processing
        
        # Development tools
        "pytest",
        "black",  # Code formatting
        "isort",  # Import sorting
        "flake8",  # Linting
        "html2text",  # For converting HTML email content to readable text
        "beautifulsoup4",  # For parsing HTML content
        "openai",  # For GPT integration
        "llama-cpp-python",  # For Llama integration
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'black',
            'isort',
            'flake8',
            'mypy',
        ],
    },
    entry_points={
        'console_scripts': [
            'gmail-assistant=gmail_assistant.gmail_voice_assistant_gui:main',
        ],
    },
    python_requires=">=3.8",
    package_data={
        'gmail_assistant': [
            'resources/*.json',
            'resources/*.pickle',
            'config/*.json',
        ],
    },
    include_package_data=True,
)

# Run post-installation tasks
if "install" in sys.argv:
    post_install()