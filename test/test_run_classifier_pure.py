# 程序主入口
from pathlib import Path

from app.utils import fm
from test_run_deepmini import run_deepmini


if __name__ == "__main__":
    fix_class = {"nsfw":"nsfw_anime", "sus":"sexy_anime", "safe":"sfw_anime"}
    for content in run_deepmini():
        img_path = content.img_path
        fm.move_file(Path(img_path), fix_class[content.img_tags[-1][0]])
