from pydantic import BaseModel
from pathlib import Path

class TagItem(BaseModel):
    """返回数据格式img_path: str | Path, img_tags: list[str]"""
    img_path: str | Path
    img_tags: list[str]

from .data_loader import PACKAGE_PATH
def get_supported_languages() -> list[str]:
    return [*map(lambda f: f.stem.removeprefix("tags_"),
                 PACKAGE_PATH.joinpath("tags").glob("tags_*.txt"))]


SUPPORTED_LANGUAGES = get_supported_languages()
from typing import Literal
class TagLanguage(BaseModel):
    """规范在tags文件夹内查找对应语言的文件,可选项则为文件tags_x.txt中的x"""
    lang: Literal[*SUPPORTED_LANGUAGES]