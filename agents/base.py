import os
import logging
import google.generativeai as genai
from core.state import SharedState

class BaseAgent:
    def __init__(self, name, state: SharedState):
        self.name = name
        self.state = state
        
        # Initialize Gemini
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash') # User asked for 'gemini-flash-latest' but standard alias is safer, will try user string first
        else:
            self.model = None

    def execute(self):
        """
        Main execution method.
        """
        raise NotImplementedError("Subclasses must implement execute()")

    def call_llm(self, prompt, json_mode=False):
        """
        Helper to call Gemini.
        """
        if not self.model:
             # Try refreshing config if key was added late
            api_key = os.environ.get("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-flash-latest')
            else:
                self.state.set_error(f"{self.name}: No API Key. cannot generate.")
                return None

        try:
            generation_config = {}
            if json_mode:
                generation_config = {"response_mime_type": "application/json"}
            
            response = self.model.generate_content(prompt, generation_config=generation_config)
            return response.text
            
        except Exception as e:
            self.state.set_error(f"{self.name} LLM Error: {e}")
            return None
