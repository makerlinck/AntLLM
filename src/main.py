from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from src.api.routers import router
from src.core import config_glob
from src.models.Deepmini.evaluation import init_pool, shutdown_pool
@asynccontextmanager
async def lifespan(_app: FastAPI):  # 将参数名改为 app_instance
    init_pool()
    yield
    shutdown_pool()

app = FastAPI(lifespan=lifespan)
@app.get("/")
async def root():
    return f"{config_glob.app_name} is Running :)"
@app.get("/info")
async def get_config():
    return config_glob
@app.get("/ping")
async def pong():
    return "Pong!"

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app)
