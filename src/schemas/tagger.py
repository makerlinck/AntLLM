from pathlib import Path
from typing import Literal
from pydantic import BaseModel

class TagItem(BaseModel):
    img_path: str | Path
    img_tags: list[str]

SUPPORTED_TAG_LANG = Literal["en","zh_cn"]
class TaggerQuery(BaseModel):
    tag_language: SUPPORTED_TAG_LANG
    query_uris: list[str]


class TagTranslatorQuery(BaseModel):
    from_to_: tuple[SUPPORTED_TAG_LANG, SUPPORTED_TAG_LANG]
    query_tags: list[str]
    translate_method: Literal["llm", "dict", "both"]

class TaggerResponse(BaseModel):
    response: list[TagItem]
    EOF: bool = False