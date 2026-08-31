import os
from dotenv import load_dotenv

load_dotenv()

# Set LangSmith environment variables
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGSMITH_TRACING", "true")
os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "skillbridge")

def is_langsmith_enabled():
    """Check if LangSmith tracing is enabled"""
    return bool(os.getenv("LANGSMITH_API_KEY")) and os.getenv("LANGSMITH_TRACING", "true").lower() == "true"

def get_langsmith_status():
    """Get LangSmith configuration status"""
    return {
        "enabled": is_langsmith_enabled(),
        "project": os.getenv("LANGSMITH_PROJECT", "skillbridge"),
        "endpoint": os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    }