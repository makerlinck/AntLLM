from pathlib import Path
from pydantic import BaseModel

class TagItem(BaseModel):
    img_path: str | Path
    img_tags: list[tuple[str, float]]

class TaggerQueryForm(BaseModel):
    query_uris: list[str]

class TaggerResponse(BaseModel):
    response: list[TagItem]