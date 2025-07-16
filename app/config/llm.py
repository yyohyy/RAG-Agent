from langchain_ollama import OllamaLLM
from app.common.variables import variables

def get_llm():
    return OllamaLLM(model=variables.OLLAMA_LLM_MODEL)
