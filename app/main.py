from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
