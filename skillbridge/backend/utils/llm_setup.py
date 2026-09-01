import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# LangSmith auto-tracing is activated by environment variables:
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=lsv2_pt_...
# LANGCHAIN_PROJECT=skillbridge-sih-2024
# All LangChain/LangGraph calls will automatically appear in LangSmith.

def get_llm():
    """Primary reasoning model — Llama 3.3 70B (traced by LangSmith)"""
    try:
        from langchain_groq import ChatGroq
        return ChatGroq(
            temperature=0.4,
            model_name="llama-3.3-70b-versatile",
            groq_api_key=GROQ_API_KEY,
        )
    except Exception:
        import groq
        client = groq.Groq(api_key=GROQ_API_KEY)
        class Wrapper:
            def invoke(self, prompt):
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": str(prompt)}],
                )
                class M:
                    content = res.choices[0].message.content
                return M()
        return Wrapper()

def get_fast_llm():
    """Fast model — Llama 3.1 8B (traced by LangSmith)"""
    try:
        from langchain_groq import ChatGroq
        return ChatGroq(
            temperature=0.3,
            model_name="llama-3.1-8b-instant",
            groq_api_key=GROQ_API_KEY,
        )
    except Exception:
        import groq
        client = groq.Groq(api_key=GROQ_API_KEY)
        class Wrapper:
            def invoke(self, prompt):
                res = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": str(prompt)}],
                )
                class M:
                    content = res.choices[0].message.content
                return M()
        return Wrapper()

get_fast_model = get_fast_llm
