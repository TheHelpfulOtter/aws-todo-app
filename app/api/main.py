import os
import boto3
import time

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from mangum import Mangum
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
from boto3.dynamodb.conditions import Key

app = FastAPI(root_path="/dev/")
handler = Mangum(app)

################################################################################
# Models
################################################################################


class PutTaskRequest(BaseModel):
    content: str  # Description of todo item.
    user_id: Optional[str] = None
    task_id: Optional[str] = None
    completed: bool = False


################################################################################
# API Endpoints
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
################################################################################


# Root
@app.get("/")
async def root():
    return {"message": "Hello World"}


# Create task
@app.put("/create-task")
async def create_task(put_task_request: PutTaskRequest):
    time_created = int(time.time())

    item = {
        "user_id": {"S": put_task_request.user_id},
        "content": {"S": put_task_request.content},
        "completed": {"BOOL": False},  # Task should be incomplete by default.
        "time_created": {"N": time_created},
        "task_id": {
            "S": f"task_{uuid4().hex}"
        },  # hex creates a string representation of the UUID without hyphens or any other separators.
        "ttl": {
            "N": int(time_created + 86400)
        },  # Task will expire and delete after 24 hours.
    }

    # Put the task into the table.
    table = _get_table()
    table.put_item(Item=item)

    # Return value for use in frontend.
    return {"task": item}


# Update task
@app.put("/update-task")
async def update_task(put_task_request: PutTaskRequest):
    # Update the task in the table.
    table = _get_table()
    table.update_item(
        Key={"task_id": {"S": put_task_request.task_id}},
        UpdateExpression="SET content = :content, completed = :completed",
        ExpressionAttributeValues={
            ":content": put_task_request.content,
            ":completed": put_task_request.completed,
        },
        ReturnValues="ALL_NEW",
    )
    return {"updated_task_id": put_task_request.task_id}


# Delete specific task via task id
@app.delete("/delete-task/{task_id}")
async def delete_task(task_id: str):
    # Delete the task from the table.
    table = _get_table()
    table.delete_item(Key={"task_id": {"S": task_id}})
    return {"deleted_task_id": task_id}


# Get specific task from task id
@app.get("/get-task/{task_id}")
async def get_task(task_id: str):
    # Get the task from the table.
    table = _get_table()
    response = table.get_item(Key={"task_id": {"S": task_id}})

    item = response.get("Item")

    if not item:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    return item


# List tasks associated with user id
@app.get("/list-tasks/{user_id}")
async def list_tasks(user_id: str):
    # List the top N tasks from the table, using the user index.
    table = _get_table()
    response = table.query(
        TableName="Tasks",
        IndexName="UserIndex",
        KeyConditionExpression="user_id = :user_id",
        ExpressionAttributeValues={":user_id": {"S": user_id}},
        ScanIndexForward=False,
        Limit=10,
    )

    items = response["Items"]
    return items


# List Tasks via User ID
# @app.get("/list-tasks/{user_id}")
# def get_user_tasks(user_id: str):
#     dynamodb = boto3.client("dynamodb")
#     query = f"SELECT * FROM Tasks WHERE user_id = '{user_id}'"
#     response = dynamodb.execute_statement(Statement=query)
#     items = response["Items"]
#     return items


# Create the dynamodb client
def _get_table():
    # table_name = os.environ.get("DYNAMODB_TABLE_NAME")  # Gets table name from output.tf
    table_name = "Tasks"
    return boto3.client("dynamodb").Table(table_name)


# Start Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
