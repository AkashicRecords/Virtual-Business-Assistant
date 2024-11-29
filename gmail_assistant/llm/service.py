"""LLM service for analyzing and processing commands using Ollama/Llama."""
import requests
import time
from ..utils import logger, handle_errors

class LLMService:
    def __init__(self, max_retries=3):
        self.context = {}
        self.ollama_url = "http://localhost:11434/api/generate"
        self.is_ollama_available = False
        logger.info("Initializing LLM Service with Ollama")
        
        # Try to connect to Ollama with retries
        for attempt in range(max_retries):
            try:
                self._test_ollama_connection()
                self.is_ollama_available = True
                break
            except ConnectionError as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    logger.warning("Falling back to rule-based processing (Ollama not available)")
                    # Don't raise the error, just continue without Ollama
        
    def _test_ollama_connection(self):
        """Test connection to Ollama server"""
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": "llama2",
                    "prompt": "test",
                    "stream": False
                },
                timeout=5  # Add timeout
            )
            if response.status_code == 200:
                logger.info("Successfully connected to Ollama")
            else:
                logger.warning(f"Failed to connect to Ollama. Status code: {response.status_code}")
                raise ConnectionError("Could not connect to Ollama server")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Could not connect to Ollama server: {str(e)}")
            raise ConnectionError("Could not connect to Ollama server")
    
    @handle_errors
    def analyze_query(self, text):
        """Analyze the user's query using Llama or fallback to rule-based"""
        logger.info(f"Analyzing query: {text}")
        
        # If Ollama is not available, use rule-based analysis
        if not self.is_ollama_available:
            return self._rule_based_analysis(text)
            
        try:
            # Attempt LLM analysis
            system_prompt = "You are a Gmail voice assistant. Analyze the user's command and categorize it."
            prompt = f"{system_prompt}\n\nUser command: {text}\n\nAnalyze the command type and any parameters."
            
            response = requests.post(
                self.ollama_url,
                json={
                    "model": "llama2",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=10
            )
            
            if response.status_code == 200:
                llm_response = response.json()
                analysis = {
                    'query_type': self._determine_query_type(text, llm_response),
                    'parameters': self._extract_parameters(text, llm_response),
                    'confidence': self._calculate_confidence(llm_response),
                }
                return analysis
                
        except Exception as e:
            logger.warning(f"LLM analysis failed, falling back to rule-based: {str(e)}")
            
        # Fallback to rule-based analysis
        return self._rule_based_analysis(text)
    
    def _rule_based_analysis(self, text):
        """Simple rule-based analysis when LLM is not available"""
        text = text.lower()
        query_type = self._determine_query_type(text, None)
        parameters = self._extract_parameters(text, None)
        
        return {
            'query_type': query_type,
            'parameters': parameters,
            'confidence': 0.7 if query_type != 'unknown' else 0.0
        }
    
    def update_context(self, new_context):
        """Update the conversation context"""
        self.context.update(new_context)
    
    def _determine_query_type(self, text, llm_response):
        """Determine the type of query based on text and LLM response"""
        text = text.lower()
        
        # First try direct keyword matching
        if 'read' in text or 'check' in text:
            return 'email_read'
        elif 'send' in text or 'compose' in text:
            return 'email_send'
        elif 'search' in text or 'find' in text:
            return 'email_search'
        elif 'improve' in text or 'suggestion' in text:
            return 'improve_writing'
            
        # If no direct match, analyze LLM response
        response_text = llm_response.get('response', '').lower()
        if 'read' in response_text or 'check' in response_text:
            return 'email_read'
        elif 'send' in response_text or 'compose' in response_text:
            return 'email_send'
        elif 'search' in response_text or 'find' in response_text:
            return 'email_search'
        elif 'improve' in response_text or 'suggestion' in response_text:
            return 'improve_writing'
            
        return 'unknown'
    
    def _extract_parameters(self, text, llm_response):
        """Extract relevant parameters from the query and LLM response"""
        params = {}
        text = text.lower()
        
        # Extract email recipient if present
        if 'to' in text:
            words = text.split()
            try:
                to_index = words.index('to')
                if to_index + 1 < len(words):
                    params['recipient'] = words[to_index + 1]
            except ValueError:
                pass
        
        # Try to extract additional parameters from LLM response
        response_text = llm_response.get('response', '')
        if 'recipient:' in response_text.lower():
            try:
                recipient = response_text.split('recipient:')[1].split()[0]
                params['recipient'] = recipient
            except:
                pass
                
        return params
    
    def _calculate_confidence(self, llm_response):
        """Calculate confidence score for the analysis"""
        # Basic confidence calculation
        if llm_response and 'response' in llm_response:
            # If we got a non-empty response, consider it relatively confident
            return 0.8 if len(llm_response['response'].strip()) > 0 else 0.0
        return 0.0

    def improve_writing(self, text):
        """Improve the writing of a given text"""
        try:
            prompt = f"Please improve the following text while maintaining its meaning:\n\n{text}"
            
            response = requests.post(
                self.ollama_url,
                json={
                    "model": "llama2",
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', text)  # Return original text if no improvement
            else:
                logger.error(f"Error improving writing: {response.status_code}")
                return text
                
        except Exception as e:
            logger.error(f"Error in improve_writing: {str(e)}")
            return text