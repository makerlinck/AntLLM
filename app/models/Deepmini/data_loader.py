from pathlib import Path

from app.utils import fm

# 配置 #
ALLOW_GPU = True
THRESHOLD = 0.618
MODEL_PROJECT_PATH = fm.work_dir / "data" / "tagger_model"

# END #
def load_tags():
    tags_path = MODEL_PROJECT_PATH / "tags.txt"
    with open(tags_path, "r") as tags_stream:
        tags = [tag for tag in (tag.strip() for tag in tags_stream) if tag]
        return tags

def load_model_from_project():
    model_path = MODEL_PROJECT_PATH / "model-resnet_custom_v4.h5"
    return model_path

if __name__ == "__main__":
    print(MODEL_PROJECT_PATH)
    print(load_tags())