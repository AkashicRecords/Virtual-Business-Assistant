"""GUI implementation using CustomTkinter."""
import customtkinter as ctk
from .voice_assistant import GmailVoiceAssistant
from .utils import handle_errors, logger
import threading
import os

class EmailCompositionWindow:
    def __init__(self, parent, assistant):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Compose Email")
        self.window.geometry("600x400")
        self.assistant = assistant
        self.setup_widgets()

    def setup_widgets(self):
        # To field
        self.to_label = ctk.CTkLabel(self.window, text="To:")
        self.to_label.pack(padx=10, pady=5)
        self.to_entry = ctk.CTkEntry(self.window, width=400)
        self.to_entry.pack(padx=10, pady=5)

        # Subject field
        self.subject_label = ctk.CTkLabel(self.window, text="Subject:")
        self.subject_label.pack(padx=10, pady=5)
        self.subject_entry = ctk.CTkEntry(self.window, width=400)
        self.subject_entry.pack(padx=10, pady=5)

        # Message body
        self.body_label = ctk.CTkLabel(self.window, text="Message:")
        self.body_label.pack(padx=10, pady=5)
        self.body_text = ctk.CTkTextbox(self.window, width=400, height=200)
        self.body_text.pack(padx=10, pady=5)

        # Send button
        self.send_button = ctk.CTkButton(self.window, text="Send", command=self.send_email)
        self.send_button.pack(pady=10)

    def send_email(self):
        to = self.to_entry.get()
        subject = self.subject_entry.get()
        body = self.body_text.get("1.0", "end-1c")
        self.assistant.send_email(to, subject, body)
        self.window.destroy()

class GmailAssistantGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Gmail Voice Assistant")
        self.assistant = GmailVoiceAssistant()
        self.setup_gui()
        
        # Set icon
        icon_path = os.path.join(os.path.dirname(__file__), 'resources', 
                               'icon.ico' if os.name == 'nt' else 'icon.icns')
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

    @handle_errors
    def setup_gui(self):
        # Status label
        self.status_label = ctk.CTkLabel(self.root, text="Status: Ready")
        self.status_label.pack(pady=10)

        # Command output
        self.output_text = ctk.CTkTextbox(self.root, width=400, height=200)
        self.output_text.pack(padx=10, pady=10)

        # Control buttons
        self.button_frame = ctk.CTkFrame(self.root)
        self.button_frame.pack(pady=10)

        self.start_button = ctk.CTkButton(
            self.button_frame, 
            text="Start Listening", 
            command=self.toggle_listening
        )
        self.start_button.pack(side="left", padx=5)

        self.help_button = ctk.CTkButton(
            self.button_frame,
            text="Show Commands",
            command=self.show_commands
        )
        self.help_button.pack(side="left", padx=5)

        self.is_listening = False
        self.listen_thread = None

    def toggle_listening(self):
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()

    def start_listening(self):
        self.is_listening = True
        self.start_button.configure(text="Stop Listening")
        self.status_label.configure(text="Status: Listening...")
        self.listen_thread = threading.Thread(target=self.listen_loop)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def stop_listening(self):
        self.is_listening = False
        self.start_button.configure(text="Start Listening")
        self.status_label.configure(text="Status: Ready")

    def listen_loop(self):
        while self.is_listening:
            command = self.assistant.listen()
            if command:
                self.output_text.insert("end", f"Command: {command}\n")
                self.assistant.process_command(command)

    def show_commands(self):
        commands = "\n".join([f"• {cmd}" for cmd in self.assistant.commands.keys()])
        self.output_text.insert("end", f"\nAvailable commands:\n{commands}\n")

def main():
    """Entry point for the application."""
    app = GmailAssistantGUI()
    app.root.mainloop()

if __name__ == "__main__":
    main() 