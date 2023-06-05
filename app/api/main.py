from fastapi import FastAPI
from fastapi.responses import JSONResponse
from mangum import Mangum
import os

app = FastAPI()
handler = Mangum(app)

stage = os.environ.get("STAGE", "dev")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users")
async def get_users():
    return {"message": "Get Users!"}


@app.get("/update")
async def get_users():
    return {"message": "The image has been updated!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
