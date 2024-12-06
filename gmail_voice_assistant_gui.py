import tkinter as tk
from tkinter import ttk, scrolledtext
import customtkinter as ctk
from original_assistant import * # Your existing voice assistant logic

class GmailVoiceAssistantGUI:
    def __init__(self):
        logger.info("Initializing GUI...")
        try:
            self.assistant = GmailVoiceAssistant()
            # Initialize main window
            self.window = ctk.CTk()
            self.window.title("Gmail Voice Assistant")
            self.window.geometry("600x400")
            
            # Initialize voice assistant components
            self.gmail_service = authenticate_gmail()
            self.engine = pyttsx3.init()
            
            self.create_widgets()
        except GmailAssistantError as e:
            logger.warning(f"NLU processing test failed: {e}. Continuing with limited functionality...")
            self.assistant = GmailVoiceAssistant(skip_nlu_test=True)
        except Exception as e:
            logger.error(f"Failed to initialize GUI: {e}")
            raise
        
    def create_widgets(self):
        # Status Frame
        self.status_frame = ctk.CTkFrame(self.window)
        self.status_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text="Status: Ready",
            font=("Arial", 14)
        )
        self.status_label.pack(side='left', padx=5)
        
        # Control Buttons
        self.button_frame = ctk.CTkFrame(self.window)
        self.button_frame.pack(fill='x', padx=10, pady=5)
        
        self.listen_button = ctk.CTkButton(
            self.button_frame,
            text="Start Listening",
            command=self.toggle_listening,
            font=("Arial", 14)
        )
        self.listen_button.pack(side='left', padx=5)
        
        self.send_email_button = ctk.CTkButton(
            self.button_frame,
            text="Send Email",
            command=self.send_email_gui,
            font=("Arial", 14)
        )
        self.send_email_button.pack(side='left', padx=5)
        
        # Output Area
        self.output_frame = ctk.CTkFrame(self.window)
        self.output_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.output_area = ctk.CTkTextbox(
            self.output_frame,
            wrap='word',
            font=("Arial", 12)
        )
        self.output_area.pack(fill='both', expand=True, padx=5, pady=5)
        
    def toggle_listening(self):
        if self.listen_button.cget("text") == "Start Listening":
            self.listen_button.configure(text="Stop Listening")
            self.status_label.configure(text="Status: Listening...")
            self.start_listening()
        else:
            self.listen_button.configure(text="Start Listening")
            self.status_label.configure(text="Status: Stopped")
            # Add stop listening logic
            
    def start_listening(self):
        command = listen_for_command()
        if command:
            self.output_area.insert('end', f"Command: {command}\n")
            response = process_command(command)
            self.output_area.insert('end', f"Response: {response}\n\n")
            self.speak(response)
        self.window.after(100, self.start_listening)
            
    def send_email_gui(self):
        # Create email dialog window
        email_window = ctk.CTkToplevel(self.window)
        email_window.title("Send Email")
        email_window.geometry("400x300")
        
        # Email form fields
        ctk.CTkLabel(email_window, text="To:").pack(padx=5, pady=2)
        to_entry = ctk.CTkEntry(email_window)
        to_entry.pack(fill='x', padx=5, pady=2)
        
        ctk.CTkLabel(email_window, text="Subject:").pack(padx=5, pady=2)
        subject_entry = ctk.CTkEntry(email_window)
        subject_entry.pack(fill='x', padx=5, pady=2)
        
        ctk.CTkLabel(email_window, text="Message:").pack(padx=5, pady=2)
        message_text = ctk.CTkTextbox(email_window, height=100)
        message_text.pack(fill='both', expand=True, padx=5, pady=2)
        
        def send():
            # Get values and send email
            to = to_entry.get()
            subject = subject_entry.get()
            message = message_text.get("1.0", 'end')
            # Use your existing send_email function
            response = send_email(to, subject, message)
            self.output_area.insert('end', f"Email Status: {response}\n\n")
            email_window.destroy()
            
        ctk.CTkButton(
            email_window,
            text="Send",
            command=send
        ).pack(pady=10)
        
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = GmailVoiceAssistantGUI()
    app.run() 