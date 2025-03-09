from fastapi import FastAPI, APIRouter
from app.schemas import tagger
from app.core import config_glob
from app.models import

app = FastAPI()

router = APIRouter(
    prefix="/api",
    tags=["API ENTRANCE"],
)

@router.post("/tagger/", response_model=tagger.TaggerResponse)
async def tag_files(body: tagger.TaggerForm):
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
