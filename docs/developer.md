# Developer Documentation

## Setup Development Environment

1. Clone the repository:
```bash
git clone [repository-url]
cd gmail-voice-assistant
```

2. Install dependencies:
```bash
pip install -e .
```

3. Run tests:
```bash
python -m pytest tests/
```

4. Build application:
```bash
./build.sh
```

## Project Structure
```
gmail-voice-assistant/
├── gmail_assistant/
│   ├── __init__.py
│   ├── gui.py
│   ├── voice_assistant.py
│   └── resources/
├── tests/
│   └── test_package.py
├── build.py
├── build.sh
└── setup.py
``` 