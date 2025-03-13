from pathlib import Path
from typing import Literal
from pydantic import BaseModel
from src.models.Deepmini import TagLanguage as ITagLanguage, TagItem as ITagItem


class TagItem(ITagItem):
    pass


class TagLanguage(ITagLanguage):
    pass


class TaggerQuery(BaseModel):
    tag_language: str
    query_uris: list[str]


class TagTranslatorQuery(BaseModel):
    from_to_: tuple[TagItem, TagItem]
    query_tags: list[str]
    translate_method: Literal["llm", "dict", "both"]


class TaggerResponse(BaseModel):
    response: list[TagItem]
    EOF: bool = False
