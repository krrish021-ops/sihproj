# Test Groq
from utils.llm_setup import LLMConfig

def test_groq():
    print("Testing Groq Connection...")
    
    llm = LLMConfig()
    model = llm.get_fast_model()
    
    response = model.invoke("Say 'Hello from Groq!'")
    print(f"Response: {response.content}")
    print("✅ Groq is working!")

if __name__ == "__main__":
    test_groq()