from pydantic import BaseModel


class Settings(BaseModel):
    database_url: str = "sqlite:///./app.db"
    local_ollama_base_url: str = "http://127.0.0.1:11434"
    tagger_model_dir = "./data/tagger_model"