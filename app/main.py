import asyncio
from pathlib import Path
from typing import AsyncIterator, Generator, AsyncGenerator

from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel

from app.core import config_glob
from app.models.deepmini import aget_evaluation

app = FastAPI()

router = APIRouter(
    prefix="/api",
    tags=["API ENTRANCE"],
)
# TODO 增加处理分发
MAX_URI_COUNT = 64

class TaggerForm(BaseModel):
    query_uris: list[str]

class TagItem(BaseModel):
    img_path: str
    img_tags: list[tuple[str, float]]

class TaggerResponse(BaseModel):
    response: list[TagItem]
@router.post("/tagger/", response_model=TaggerResponse)
async def tag_files(body: TaggerForm):
    uri_list, res_list = [], []
    for uri in body.query_uris:
        uri_list.append(uri.strip("\u202a"))
    for item in aget_evaluation(uri_list, return_path=False):
        print(res_list.append({"img_path":item["img_path"],"img_tags":item["img_tags"][1:]}))
    return {"response": res_list}

app.include_router(router)

@app.get("/")
async def root():
    return f"{config_glob.app_name} is Running :)"
@app.get("/info")
async def get_config():
    return config_glob
@app.get("/ping")
async def pong():
    return "Pong!"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
