from typing import Literal

from src import SUPPORTED_TAG_LANG
from src.utils import fm

# 配置 #
ALLOW_GPU = True # 是否使用GPU
THRESHOLD = 0.618 # 预测置信度阈值,越高则越精确，但预测内容会变少,对当前代码来说过高的阈值可能会使进程崩溃，建议0.5+-0.7
MODEL_PROJECT_PATH = fm.work_dir / "data" / "tagger_model" # Danbooru模型文件路径
MAX_TASK_COUNT = 2 # 最大多进程并发数

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