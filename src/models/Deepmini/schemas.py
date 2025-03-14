from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from .data_loader import PACKAGE_PATH


class TagItem(BaseModel):
    """返回数据格式img_path: str | Path, img_tags: list[str]"""
    img_seq: tuple[int, str | Path ]  # img sequence number
    img_tags: list[str]  # img tag-list

def get_supported_languages() -> list[str]:
    return [*map(lambda f: f.stem.removeprefix("tags_"),
                 PACKAGE_PATH.joinpath("tags").glob("tags_*.txt"))]
pass


SUPPORTED_LANGUAGES = get_supported_languages()


class TagLanguage(BaseModel):
    """规范在tags文件夹内查找对应语言的文件,可选项则为文件tags_x.txt中的x"""
    lang: Literal[*SUPPORTED_LANGUAGES]
