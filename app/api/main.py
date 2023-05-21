from fastapi import FastAPI
from mangum import Mangum
import os

app = FastAPI()

stage = os.environ.get('STAGE', 'dev')

@app.get("/")
async def root():
    return {"status": 200, "message": "If you can see this, hi!"}

@app.get("/test")
async def test_route():
    return {"message": "Why, hello there."}

handler = Mangum(app)