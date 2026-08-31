# LLM Setup
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

class LLMConfig:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        
    def get_main_model(self, temperature=0.3):
        return ChatGroq(
            api_key=self.api_key,
            model="llama-3.3-70b-versatile",
            temperature=temperature,
            max_tokens=2048,
        )
    
    def get_fast_model(self, temperature=0.2):
        return ChatGroq(
            api_key=self.api_key,
            model="llama-3.1-8b-instant",
            temperature=temperature,
            max_tokens=1024,
        )