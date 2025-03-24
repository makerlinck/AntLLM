from typing import Literal
from pydantic import BaseModel
from src.models.Deepmini import TagLanguage as ITagLanguage, TagItem as ITagItem,SUPPORTED_TAG_LANGUAGES as LANGS


class TagItem(ITagItem):
    pass

class TagLanguage(ITagLanguage):
    pass


class TaggerQuery(BaseModel):
    tag_language: Literal[*LANGS]
    query_uris: list[str]


class TagTranslatorQuery(BaseModel):
    from_to_: tuple[Literal[*LANGS],Literal[*LANGS]]
    query_tags: list[str]
    translate_method: Literal["llm", "dict", "both"]


class TaggerResponse(BaseModel):
    response: list[TagItem]
