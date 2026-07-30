from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import sqlite3

app=FastAPI()

cx=sqlite3.connect("tasks.db",check_same_thread=False)
cu=cx.cursor()
cu.execute("Create table if not exists tasks(id INTEGER PRIMARY KEY,title TEXT,done BOOLEAN)")
cx.commit()
cu.execute("SELECT COUNT(*) FROM tasks")
count=cu.fetchone()
if count[0]==0:
    cu.execute("INSERT INTO tasks (title,done) VALUES (?,?)",("study",1))
    cu.execute("INSERT INTO tasks (title,done) VALUES (?,?)",("workout",0))
    cu.execute("INSERT INTO tasks (title,done) VALUES (?,?)",("meal prep",0))
    cx.commit()

class TaskCreate(BaseModel):
    title:str

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

def find_task(id):
    cu.execute("SELECT * FROM tasks WHERE id = ?",(id,))
    task=cu.fetchone()
    return task

def row_to_dict(row):
    return {"id":row[0],"title":row[1],"done":bool(row[2])}

@app.get("/")
def root():
    return {"name":"Task API","version":"1.0","endpoints":["/tasks"]}

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/tasks",description="List all tasks")
def get_tasks():
    cu.execute("SELECT * FROM tasks")
    rows=cu.fetchall()
    return [row_to_dict(row) for row in rows]

@app.post("/tasks",status_code=201,description="Create a new task")
def create_task(task: TaskCreate):
    if task.title.strip()=="":
        raise HTTPException(status_code=400,detail="Task title seems to be empty")
    cu.execute("INSERT INTO tasks (title,done) VALUES (?,?)",(task.title,0))
    cx.commit()
    new_id=cu.lastrowid
    new_task={"id":new_id,"title":task.title,"done":False}
    return {"new_task": new_task}

@app.get("/tasks/{id}",description="Search a task")
def get_task(id: int):
    task=find_task(id)
    if task is None:
        raise HTTPException(status_code=404,detail=f"Task {id} not found")
    return {"task":row_to_dict(task)}

@app.put("/tasks/{id}",description="Update a task")
def update_task(id:int ,update: TaskUpdate):
    task=find_task(id)
    if task is None:
        raise HTTPException(status_code=404,detail=f"Task {id} not found")
    if update.title is not None :
        if update.title.strip()=="":
            raise HTTPException(status_code=400,detail="Task title cannot be empty")

        cu.execute("UPDATE tasks SET title=? WHERE id =?",(update.title,id))
    if update.done is not None :
        cu.execute("UPDATE tasks SET done=? WHERE id =?",(update.done,id))
    cx.commit()
    task=find_task(id)
    return {"updated_task":row_to_dict(task)}

@app.delete("/tasks/{id}",status_code=204,description="Delete a task")
def del_task(id:int):
    task=find_task(id)
    if task is None:
        raise HTTPException(status_code=404,detail=f"Task {id} not found")
    cu.execute("DELETE FROM tasks WHERE id = ?",(id,))
    cx.commit()
