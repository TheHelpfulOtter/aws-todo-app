from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"status": 200, "message": "If you can see this, hi!"}

@app.get("/test")
async def test_route():
    return {"message": "Why, hello there."}
