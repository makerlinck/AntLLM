from fastapi import FastAPI
import uvicorn

from src.api.routers import router
from src.core import config_glob

app = FastAPI()

@app.get("/")
async def root():
    return f"{config_glob.app_name} is Running :)"
@app.get("/info")
async def get_config():
    return config_glob
@app.get("/ping")
async def pong():
    return "Pong!"

from src.models.Deepmini.evaluation import init_pool, shutdown_pool

@app.on_event("startup")
async def startup():
    """应用启动时初始化进程池"""
    init_pool()

@app.on_event("shutdown")
async def shutdown():
    """应用关闭时销毁进程池"""
    shutdown_pool()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app)
