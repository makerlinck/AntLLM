from pathlib import Path
from typing import Literal

pass
# 配置 #
PACKAGE_PATH = Path(__file__).parent # Danbooru模型文件路径
ALLOW_GPU = True # 是否使用GPU
THRESHOLD = 0.618 # 预测置信度阈值,越高则越精确，但预测内容会变少，建议设置范围:0.5+-0.7
MAX_TASKS = 4 # 最大多进程并发数
# END #
def get_supported_languages() -> list[str]:
    return [*map(lambda f: f.stem.removeprefix("tags_"),
                 PACKAGE_PATH.joinpath("tags").glob("tags_*.txt"))]

SUPPORTED_TAG_LANGUAGES = get_supported_languages()
def get_tags(lang:Literal[*SUPPORTED_TAG_LANGUAGES]):
    tag_file_path = PACKAGE_PATH.joinpath(f"tags/tags_{lang}.txt")
    with open(tag_file_path, "r",encoding="utf-8") as tags_stream:
        tags = [tag for tag in (tag.strip() for tag in tags_stream) if tag]
        return tags

def get_model_path():
    model_path = PACKAGE_PATH.joinpath("resnet-models/model-resnet_custom_v4.h5")
    if not model_path.exists():
        raise Exception(f"{model_path}: Model file not found. Please Check!")
    return model_path

if __name__ == "__main__":
    print(f"Package directory here:{PACKAGE_PATH}")
    print(get_supported_languages())
    print(get_tags("zh-cn"))
    print(get_model_path())