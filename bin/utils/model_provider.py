
from langchain_ollama import OllamaLLM
from langchain_ollama import ChatOllama
base_url = "http://127.0.0.1:11434"
def initialize_llm(model:str):
    return ChatOllama(
    model=model,
    base_url=base_url,
    temperature=0.0,
    format="json"
    )

def initialize_v_llm(model:str):
    return OllamaLLM(
    model=model,
    base_url=base_url,
    temperature=0.0,
    )

initialize_viewer_llm = initialize_v_llm(model ="llava:13b")
initialize_classifier_llm = initialize_llm(model ="qwen2.5:3b")
