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

table_name = "Tasks"
boto3_client = boto3.client("dynamodb")


# Root
@app.get("/")
async def root():
    return {"message": "Hello World"}


# Create task
@app.put("/create-task")
async def create_task(put_task_request: PutTaskRequest):
    task_id = f"task_{uuid4().hex}"
    time_created = int(time.time())
    ttl = str(time_created + 86400)

    item = {
        "user_id": {"S": put_task_request.user_id},
        "content": {"S": put_task_request.content},
        "completed": {
            "BOOL": put_task_request.completed
        },  # Task should be incomplete by default.
        "time_created": {"N": str(time_created)},
        "task_id": {
            "S": task_id
        },  # hex creates a string representation of the UUID without hyphens or any other separators.
        "ttl": {"N": ttl},  # Task will expire and delete after 24 hours.
    }

    # Put the task into the table.
    client = boto3_client
    response = client.put_item(TableName=table_name, Item=item)

    # Return value for use in frontend.
    return {"created task": item}


# Update task
@app.put("/update-task")
async def update_task(put_task_request: PutTaskRequest):
    # Update the task in the table.
    client = boto3_client
    client.update_item(
        TableName=table_name,
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
    client = boto3_client
    client.delete_item(TableName=table_name, Key={"task_id": {"S": task_id}})
    return {"deleted_task_id": task_id}


# Get specific task from task id
@app.get("/get-task/{task_id}")
async def get_task(task_id: str):
    # Get the task from the table.
    client = boto3_client
    response = client.get_item(TableName=table_name, Key={"task_id": {"S": task_id}})

    item = response.get("Item")

    if not item:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    return item


# List tasks associated with user id
@app.get("/list-tasks/{user_id}")
async def list_tasks(user_id: str):
    # List the top N tasks from the table, using the user index.
    client = boto3_client
    response = client.query(
        TableName=table_name,
        IndexName="UserIndex",
        KeyConditionExpression="user_id = :user_id",
        ExpressionAttributeValues={":user_id": {"S": str(user_id)}},
        ScanIndexForward=False,
        Limit=10,
    )
    tasks = response["Items"]

    print(response)
    print(response["Items"])

    return tasks


# List Tasks via User ID
@app.get("/list-tasks/{user_id}")
def get_user_tasks(user_id: str):
    dynamodb = boto3.client("dynamodb")
    query = f"SELECT * FROM Tasks WHERE user_id = '{user_id}'"
    response = dynamodb.execute_statement(Statement=query)
    items = response["Items"]
    return items


# Start Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
