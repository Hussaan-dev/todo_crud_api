from fastapi import FastAPI,HTTPException

app=FastAPI()

tasks= [
    {"id":1,"title":"study","done":True},
    {"id":2,"title":"workout","done":False},
    {"id":3,"title":"meal prep","done":False},
]

def find_task(id):
    for task in tasks:
        if task["id"]==id:
            return task

@app.get("/")
def root():
    return {"name":"Task API","version":"1.0","endpoints":["/tasks"]}

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/tasks")
def get_tasks():
    return {"tasks":tasks}

@app.get("/tasks/{id}")
def get_task(id: int):
    task=find_task(id)
    if task is None:
        raise HTTPException(status_code=404,detail=f"Task {id} not found")
    return {"task":task}