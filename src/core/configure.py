from pydantic import BaseModel


class Configures(BaseModel):
    app_name: str = "AntLLM"
    app_version: str = "0.1.1"
    app_description: str = "图片分类归档服务程序"

    class Config:
        env_file = ".env"
        tagger_model_path = "./data/h5model"

config_glob = Configures()