from typing import Literal

from src import SUPPORTED_TAG_LANG
from src.utils import fm

# 配置 #
ALLOW_GPU = True
THRESHOLD = 0.618
MODEL_PROJECT_PATH = fm.work_dir / "data" / "tagger_model"


TAG_LANGUAGE = "zh_cn"
# END #

def load_tags(lang:Literal[*SUPPORTED_TAG_LANG]):
    tags_path = MODEL_PROJECT_PATH / f"tags-{lang}.txt"
    with open(tags_path, "r",encoding="utf-8") as tags_stream:
        tags = [tag for tag in (tag.strip() for tag in tags_stream) if tag]
        return tags

def load_model_from_project():
    model_path = MODEL_PROJECT_PATH / "model-resnet_custom_v4.h5"
    return model_path

if __name__ == "__main__":
    print(MODEL_PROJECT_PATH)
    print(load_tags("zh_cn"))