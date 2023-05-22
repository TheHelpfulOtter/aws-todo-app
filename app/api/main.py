from fastapi import FastAPI
from mangum import Mangum
import uvicorn
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
