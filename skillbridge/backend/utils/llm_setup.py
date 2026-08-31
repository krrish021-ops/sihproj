"""
Groq LLM Configuration & Setup
==============================
Provides LLMConfig and helper functions for LangGraph agents.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class LLMConfig:
    """Configuration class for Groq LLMs used across LangGraph agents."""
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    DEFAULT_MODEL = "llama-3.3-70b-versatile"
    FAST_MODEL = "llama-3.1-8b-instant"
    ASSESSMENT_MODEL = "llama-3.3-70b-versatile"

    @classmethod
    def get_llm(cls, model_name: str = None, temperature: float = 0.3):
        model = model_name or cls.DEFAULT_MODEL
        api_key = cls.GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")
        try:
            from langchain_groq import ChatGroq
            return ChatGroq(
                groq_api_key=api_key if api_key else "gsk_placeholder_key",
                model_name=model,
                temperature=temperature,
            )
        except Exception as e:
            print(f"Notice: ChatGroq initialization ({model}): {e}")
            return None

    @classmethod
    def get_fast_llm(cls, temperature: float = 0.1):
        return cls.get_llm(model_name=cls.FAST_MODEL, temperature=temperature)

    @classmethod
    def get_assessment_llm(cls, temperature: float = 0.4):
        return cls.get_llm(model_name=cls.ASSESSMENT_MODEL, temperature=temperature)


def get_llm(model_name: str = "llama-3.3-70b-versatile", temperature: float = 0.3):
    return LLMConfig.get_llm(model_name=model_name, temperature=temperature)


def get_groq_llm(model_name: str = "llama-3.3-70b-versatile", temperature: float = 0.3):
    return LLMConfig.get_llm(model_name=model_name, temperature=temperature)


def get_chat_llm(model_name: str = "llama-3.3-70b-versatile", temperature: float = 0.3):
    return LLMConfig.get_llm(model_name=model_name, temperature=temperature)