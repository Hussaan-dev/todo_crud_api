from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app=FastAPI()

tasks= [
    {"id":1,"title":"study","done":True},
    {"id":2,"title":"workout","done":False},
    {"id":3,"title":"meal prep","done":False},
]

class TaskCreate(BaseModel):
    title:str

def find_task(id):
    for task in tasks:
        if task["id"]==id:
            return task

def find_id():
    if not tasks:
        return 1
    return max(task["id"] for task in tasks)+1

@app.get("/")
def root():
    return {"name":"Task API","version":"1.0","endpoints":["/tasks"]}

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/tasks")
def get_tasks():
    return {"tasks":tasks}

@app.post("/tasks",status_code=201)
def create_task(task: TaskCreate):
    if task.title.strip()=="":
        raise HTTPException(status_code=400,detail="Task title seems to be empty")
    next_id=find_id()
    new_task={"id":next_id,"title":task.title,"done":False}
    tasks.append(new_task)
    return {"new_task": new_task}

@app.get("/tasks/{id}")
def get_task(id: int):
    task=find_task(id)
    if task is None:
        raise HTTPException(status_code=404,detail=f"Task {id} not found")
    return {"task":task}