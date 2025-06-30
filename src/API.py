from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/hello")
async def root():
    return {"message": "Hello World"}


@app.get("/queue")
async def queue():
    return {"message": "Queue endpoint is not implemented yet"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
