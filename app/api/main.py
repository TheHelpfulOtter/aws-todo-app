from fastapi import FastAPI
from fastapi.responses import JSONResponse
from mangum import Mangum
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
from boto3.dynamodb.conditions import Key

import os
import boto3
import time

app = FastAPI(root_path="/dev/")
handler = Mangum(app)

stage = os.environ.get("STAGE", "dev")


# Models
class PutTaskRequest(BaseModel):
    content: str  # Description of todo item.
    user_id: Optional[str] = None
    task_id: Optional[str] = None
    completed: bool = False


# API Endpoints
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.put("/create-task")
async def create_task(put_task_request: PutTaskRequest):
    time_created = int(time.time())

    item = {
        "user_id": put_task_request.user_id,
        "content": put_task_request.content,
        "completed": False,  # Task should be incomplete by default.
        "time_created": time_created,
        "task_id": f"task_{uuid4().hex}",  # hex creates a string representation of the UUID without hyphens or any other separators.
        "ttl": int(time_created + 86400),  # Task will expire and delete after 24 hours.
    }

    # Put the task into the table.
    table = _get_table()
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/put_item.html
    table.put_item(Item=item)

    # Return value for use in frontend.
    return {"task": item}


@app.get("/get-task/{task_id}")
async def get_task(task_id: str):
    # Get the task from the table.
    table = _get_table()
    response = table.get_item(Key={"task_id": task_id})
    item = response.get("Item")

    if not item:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    return item


def _get_table():
    table_name = os.environ.get("DYNAMODB_TABLE_NAME")  # Gets table name from output.tf

    return boto3.resource("dynamodb").Table(table_name)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
