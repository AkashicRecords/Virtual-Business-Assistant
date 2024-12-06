# API Documentation

## Voice Assistant API
- `process_command(command: str) -> str`
- `listen() -> str`
- `speak(text: str) -> None`

## Email Service API
- `send_email(to: str, subject: str, message: str) -> str`
- `read_email(email_id: str) -> dict`
- `list_emails(query: str = None) -> list`

## LLM Service API
- `generate_response(prompt: str) -> str`
- `improve_email(content: str) -> str`
- `summarize_email(content: str) -> str`
