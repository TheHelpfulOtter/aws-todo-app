from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"status": 200, "message": "If you can see this, hi!"}
