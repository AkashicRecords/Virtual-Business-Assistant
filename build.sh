#!/bin/bash
# Build script for Gmail Voice Assistant

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Building for macOS..."
    python3 build.py
    echo "App bundle created in dist/Gmail Voice Assistant.app"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "Building for Windows..."
    python build.py
    echo "Executable created in dist/Gmail Voice Assistant.exe"
fi 