from setuptools import setup, find_packages

setup(
    name="gmail-voice-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "speech_recognition",
        "PyAudio",
        "pyttsx3",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "google-api-python-client",
        "nltk",
        "customtkinter",
        "pillow",
        "python-dotenv",
        "email-validator",
        "requests"
    ],
    entry_points={
        'console_scripts': [
            'gmail-assistant=gmail_assistant.gui:main',
        ],
    }
) 