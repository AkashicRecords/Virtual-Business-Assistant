"""LLM Service for natural language conversation using Llama with Metal acceleration."""
import os
from llama_cpp import Llama
from .error_handler import handle_errors, GmailAssistantError
import platform
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        try:
            # Get project root directory (where setup.py is)
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Default model path in project's models directory
            default_model_path = os.path.join(project_root, 'models', 'llama-2-7b-chat.Q4_K_M.gguf')
            
            # Use environment variable if set, otherwise use default path
            model_path = os.getenv('LLAMA_MODEL_PATH', default_model_path)
            
            # Create models directory if it doesn't exist
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
            if not os.path.exists(model_path):
                raise GmailAssistantError(
                    f"Llama model not found at: {model_path}\n"
                    f"Please download the model using either:\n\n"
                    f"1. curl (built-in):\n"
                    f"mkdir -p {os.path.dirname(model_path)}\n"
                    f"curl -L https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf "
                    f"-o {model_path}\n\n"
                    f"2. wget (requires 'brew install wget'):\n"
                    f"mkdir -p {os.path.dirname(model_path)}\n"
                    f"wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf "
                    f"-O {model_path}"
                )
            
            # Check if running on macOS
            is_macos = platform.system().lower() == "darwin"
            
            # Initialize Llama with Metal acceleration on macOS
            self.llm = Llama(
                model_path=model_path,
                n_ctx=4096,  # Increased context window
                n_threads=8,  # Reduced thread count when using GPU
                n_gpu_layers=-1,  # Use all layers on GPU
                use_mlock=True,  # Keep model in memory
                use_metal=is_macos,  # Enable Metal on macOS
                main_gpu=0,  # Use primary GPU
                tensor_split=None,  # Auto split between CPU/GPU
                rope_freq_scale=1.0,  # RoPE frequency scaling
                verbose=True  # Show loading progress
            )
            
            # Test the model
            logger.info("Testing LLM with a simple prompt...")
            test_response = self.llm(
                "Hello, are you working?",
                max_tokens=20,
                echo=False
            )
            logger.info(f"LLM test response: {test_response['choices'][0]['text']}")
            
            # Store conversation history
            self.conversation_history = []
            
        except Exception as e:
            raise GmailAssistantError(f"Failed to initialize Llama: {str(e)}")
        
    def _build_prompt(self, user_input):
        """Build prompt with conversation history."""
        system_prompt = """You are a helpful email assistant that can help with reading, sending, and managing emails.
        You should provide clear and concise responses and maintain context of the conversation."""
        
        # Build conversation history
        conversation = f"<s>[INST] <<SYS>>{system_prompt}<</SYS>>\n\n"
        
        # Add previous exchanges
        for exchange in self.conversation_history[-5:]:  # Keep last 5 exchanges for context
            conversation += f"User: {exchange['user']}\nAssistant: {exchange['assistant']}\n\n"
            
        # Add current input
        conversation += f"User: {user_input}\nAssistant:[/INST]"
        
        return conversation
        
    @handle_errors
    def process_conversation(self, user_input, context=None):
        """Process natural language input using Llama."""
        try:
            # Build prompt with conversation history
            prompt = self._build_prompt(user_input)
            
            # Generate response
            response = self.llm(
                prompt,
                max_tokens=512,
                temperature=0.7,
                stop=["User:", "[INST]"],
                echo=False
            )
            
            assistant_response = response['choices'][0]['text'].strip()
            
            # Store the exchange in conversation history
            self.conversation_history.append({
                'user': user_input,
                'assistant': assistant_response
            })
            
            return assistant_response
            
        except Exception as e:
            raise GmailAssistantError(f"Llama processing failed: {str(e)}")
            
    def clear_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []