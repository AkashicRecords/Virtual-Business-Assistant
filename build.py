import PyInstaller.__main__
import sys
import os
import shutil

def clean_build():
    """Clean previous builds"""
    for dir in ['build', 'dist']:
        if os.path.exists(dir):
            shutil.rmtree(dir)

def build_app():
    """Build standalone executable"""
    clean_build()
    
    common_options = [
        'gmail_assistant/gui.py',
        '--onefile',
        '--windowed',
        '--name=Gmail Voice Assistant',
        '--hidden-import=pyttsx3.drivers',
        '--hidden-import=pyttsx3.drivers.dummy',
        '--hidden-import=pyttsx3.drivers.espeak',
        '--hidden-import=pyttsx3.drivers.nsss',
        '--hidden-import=pyttsx3.drivers.sapi5',
    ]

    if sys.platform == "darwin":  # macOS
        PyInstaller.__main__.run(common_options + [
            '--add-binary=/opt/homebrew/lib/libportaudio.dylib:.',
            '--osx-bundle-identifier=com.gmail.voiceassistant',
            '--icon=gmail_assistant/resources/icon.icns'
        ])
    elif sys.platform == "win32":  # Windows
        PyInstaller.__main__.run(common_options + [
            '--icon=gmail_assistant/resources/icon.ico'
        ])

if __name__ == "__main__":
    build_app() 