import customtkinter as ctk
from .gmail_voice_assistant import GmailVoiceAssistant
from .error_handler import handle_errors, GmailAssistantError
import threading
import logging

logger = logging.getLogger(__name__)

class GmailVoiceAssistantGUI:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Gmail Voice Assistant")
        self.window.geometry("800x600")
        
        self.assistant = GmailVoiceAssistant()
        self.listening = False
        self.listen_thread = None
        
        self.setup_gui()
        
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
        self.status_label.configure(className="status-label")
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
        self.listen_button.configure(className="listen-button")
        self.listen_button.pack(side='left', padx=5)
        
        # Output Frame
        self.output_frame = ctk.CTkFrame(self.window)
        self.output_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.output_text = ctk.CTkTextbox(
            self.output_frame,
            font=("Arial", 12)
        )
        self.output_text.configure(className="output-text")
        self.output_text.pack(fill='both', expand=True, padx=5, pady=5)
    
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
    
    def listen_loop(self):
        """Background listening loop."""
        while self.listening:
            try:
                command = self.assistant.listen()
                if command:
                    self.log_output(f"Command: {command}")
                    response = self.assistant.process_command(command)
                    self.log_output(f"Response: {response}")
                    self.assistant.speak(response)
            except GmailAssistantError as e:
                logger.error(f"Error in listen loop: {str(e)}")
                self.log_output(f"Error: {str(e)}")
    
    def log_output(self, text):
        """Add text to output window."""
        self.output_text.insert('end', f"{text}\n")
        self.output_text.see('end')
    
    def run(self):
        """Start the GUI application."""
        self.window.mainloop()

def main():
    app = GmailVoiceAssistantGUI()
    app.run()

if __name__ == "__main__":
    main() 