import customtkinter as ctk
from .gmail_voice_assistant import GmailVoiceAssistant
from .error_handler import handle_errors, GmailAssistantError
import threading
import logging

logger = logging.getLogger(__name__)

class GmailAssistantGUI:
    def __init__(self):
        try:
            logger.info("Initializing GUI...")
            self.window = ctk.CTk()
            self.window.title("Gmail Voice Assistant")
            self.window.geometry("800x600")
            
            # Initialize assistant first
            logger.info("Creating voice assistant...")
            self.assistant = GmailVoiceAssistant()
            
            self.listening = False
            self.listen_thread = None
            
            logger.info("Setting up GUI components...")
            self.setup_gui()
            
            # Show comprehensive test results
            self.log_output("\n=== System Status ===")
            
            try:
                self.log_output("\n1. NLTK Components:")
                self.assistant.test_nltk_components()
                self.log_output("✓ NLP components ready")
            except GmailAssistantError as e:
                self.log_output(f"✗ NLP Error: {str(e)}")
            
            try:
                self.log_output("\n2. Gmail API:")
                self.assistant.test_api_endpoints()
                self.log_output("✓ Gmail API connected")
            except GmailAssistantError as e:
                self.log_output(f"✗ API Error: {str(e)}")
            
            try:
                self.log_output("\n3. Voice Components:")
                self.assistant.test_voice_components()
                self.log_output("✓ Voice system ready")
            except GmailAssistantError as e:
                self.log_output(f"✗ Voice Error: {str(e)}")
            
            try:
                self.log_output("\n4. NLU Processing:")
                self.assistant.test_nlu_processing()
                self.log_output("✓ NLU system operational")
            except GmailAssistantError as e:
                self.log_output(f"✗ NLU Error: {str(e)}")
            
            self.log_output("\n=== Initialization Complete ===\n")
            self.status_label.configure(text="Status: Ready")
            
            logger.info("GUI initialization complete")
            
        except Exception as e:
            logger.error(f"Failed to initialize GUI: {str(e)}")
            raise

    def setup_gui(self):
        """Setup GUI components."""
        # Status Frame
        self.status_frame = ctk.CTkFrame(self.window)
        self.status_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Status: Ready",
            font=("Arial", 14)
        )
        self.status_label.pack(side='left', padx=5)
        
        # Control Frame
        self.control_frame = ctk.CTkFrame(self.window)
        self.control_frame.pack(fill='x', padx=10, pady=5)
        
        self.listen_button = ctk.CTkButton(
            self.control_frame,
            text="Start Listening",
            command=self.toggle_listening,
            font=("Arial", 14)
        )
        self.listen_button.pack(side='left', padx=5)
        
        self.compose_button = ctk.CTkButton(
            self.control_frame,
            text="Compose Email",
            command=self.open_compose_window,
            font=("Arial", 14)
        )
        self.compose_button.pack(side='left', padx=5)
        
        # Add chat mode toggle
        self.chat_mode = False
        self.chat_button = ctk.CTkButton(
            self.control_frame,
            text="Chat Mode: Off",
            command=self.toggle_chat_mode,
            font=("Arial", 14)
        )
        self.chat_button.pack(side='left', padx=5)
        
        # Add clear chat button
        self.clear_chat_button = ctk.CTkButton(
            self.control_frame,
            text="Clear Chat",
            command=self.clear_chat,
            font=("Arial", 14)
        )
        self.clear_chat_button.pack(side='left', padx=5)
        
        # Output Frame
        self.output_frame = ctk.CTkFrame(self.window)
        self.output_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.output_text = ctk.CTkTextbox(
            self.output_frame,
            font=("Arial", 12)
        )
        self.output_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Add clear button for output
        self.clear_button = ctk.CTkButton(
            self.control_frame,
            text="Clear Output",
            command=self.clear_output,
            font=("Arial", 14)
        )
        self.clear_button.pack(side='right', padx=5)
    
    @handle_errors
    def toggle_listening(self):
        """Toggle voice listening on/off."""
        if not self.listening:
            self.listening = True
            self.listen_button.configure(text="Stop Listening")
            self.status_label.configure(text="Status: Listening...")
            self.listen_thread = threading.Thread(target=self.listen_loop)
            self.listen_thread.daemon = True
            self.listen_thread.start()
        else:
            self.listening = False
            self.listen_button.configure(text="Start Listening")
            self.status_label.configure(text="Status: Ready")
    
    def toggle_chat_mode(self):
        """Toggle between command mode and chat mode."""
        self.chat_mode = not self.chat_mode
        self.chat_button.configure(
            text=f"Chat Mode: {'On' if self.chat_mode else 'Off'}"
        )
        self.log_output(f"\nSwitched to {'Chat' if self.chat_mode else 'Command'} Mode")
        
    def clear_chat(self):
        """Clear chat history."""
        self.assistant.llm_service.clear_conversation()
        self.log_output("\nChat history cleared")
        
    def listen_loop(self):
        """Background listening loop."""
        while self.listening:
            try:
                command = self.assistant.listen()
                if command:
                    self.log_output(f"\nYou: {command}")
                    
                    if self.chat_mode:
                        # In chat mode, everything goes to LLM
                        response = self.assistant.llm_service.process_conversation(command)
                    else:
                        # In command mode, try commands first, then fall back to LLM
                        response = self.assistant.process_command(command)
                        
                    self.log_output(f"\nAssistant: {response}")
                    self.assistant.speak(response)
                    
            except GmailAssistantError as e:
                logger.error(f"Error in listen loop: {str(e)}")
                self.log_output(f"Error: {str(e)}")
                self.status_label.configure(text=f"Status: Error - {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error in listen loop: {str(e)}")
                self.log_output(f"Unexpected error: {str(e)}")
                self.listening = False
                self.listen_button.configure(text="Start Listening")
                self.status_label.configure(text="Status: Error")
    
    def log_output(self, text):
        """Add text to output window."""
        try:
            self.output_text.insert('end', f"{text}\n")
            self.output_text.see('end')
        except Exception as e:
            logger.error(f"Error logging output: {str(e)}")
    
    def clear_output(self):
        """Clear the output text area."""
        try:
            self.output_text.delete('1.0', 'end')
        except Exception as e:
            logger.error(f"Error clearing output: {str(e)}")
    
    def open_compose_window(self):
        """Open email composition window."""
        try:
            # Placeholder for email composition functionality
            self.log_output("Opening email composition window...")
            # TODO: Implement email composition window
        except Exception as e:
            logger.error(f"Error opening compose window: {str(e)}")
            self.log_output(f"Error opening compose window: {str(e)}")
    
    def run(self):
        """Start the GUI application."""
        try:
            self.window.mainloop()
        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}")
            raise

def main():
    try:
        app = GmailAssistantGUI()
        app.run()
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")
        raise

if __name__ == "__main__":
    main() 