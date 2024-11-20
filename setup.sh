#!/bin/bash

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install package in development mode
pip install -e .

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')" 