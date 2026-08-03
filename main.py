from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,EmailStr
import psycopg
from dotenv import load_dotenv
import os
from supabase import create_client

app=FastAPI()
load_dotenv()

DATABASE_URL=os.environ.get('DATABASE_URL')
SUPABASE_URL=os.environ.get('SUPABASE_URL')
SUPABASE_KEY=os.environ.get('SUPABASE_KEY')

if not DATABASE_URL:
    raise RuntimeError("Missing DATABASE_URL")
if not (SUPABASE_URL and SUPABASE_KEY):
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY")

supabase=create_client(SUPABASE_URL,SUPABASE_KEY)
cx=psycopg.connect(DATABASE_URL)
cu=cx.cursor()
cu.execute("Create table if not exists tasks(id SERIAL PRIMARY KEY,title TEXT,done BOOLEAN)")
cx.commit()
cu.execute("SELECT COUNT(*) FROM tasks")
count=cu.fetchone()
if count[0]==0:
    cu.execute("INSERT INTO tasks (title,done) VALUES (%s,%s)",("study",True))
    cu.execute("INSERT INTO tasks (title,done) VALUES (%s,%s)",("workout",False))
    cu.execute("INSERT INTO tasks (title,done) VALUES (%s,%s)",("meal prep",False))
    cx.commit()

class TaskCreate(BaseModel):
    title:str

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

class Auth(BaseModel):
    email: EmailStr
    password: str

def find_task(id):
    cu.execute("SELECT * FROM tasks WHERE id = %s",(id,))
    task=cu.fetchone()
    return task

def row_to_dict(row):
    return {"id":row[0],"title":row[1],"done":bool(row[2])}

@app.post("/auth/signup",status_code=201)
def signup(cred: Auth):
    if cred.password.strip()=="":
            raise HTTPException(status_code=400,detail="Missing password")
    try:
        result=supabase.auth.sign_up({"email":cred.email,"password":cred.password})
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    return result

@app.post("/auth/login",status_code=200)
def login(cred: Auth):
    if cred.password.strip()=="":
            raise HTTPException(status_code=400,detail="Missing password")
    try:
        result=supabase.auth.sign_in_with_password({"email":cred.email,"password":cred.password})
    except Exception:
        raise HTTPException(status_code=401,detail="Invalid login credentials")
    return result

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
    cu.execute("INSERT INTO tasks (title,done) VALUES (%s,%s) RETURNING *",(task.title,False))
    last_row=cu.fetchone()
    cx.commit()
    return {"new_task": row_to_dict(last_row)}

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
        cu.execute("UPDATE tasks SET title=%s WHERE id =%s",(update.title,id))
    if update.done is not None :
        cu.execute("UPDATE tasks SET done=%s WHERE id =%s",(update.done,id))
    cx.commit()
    task=find_task(id)
    return {"updated_task":row_to_dict(task)}

@app.delete("/tasks/{id}",status_code=204,description="Delete a task")
def del_task(id:int):
    task=find_task(id)
    if task is None:
        raise HTTPException(status_code=404,detail=f"Task {id} not found")
    cu.execute("DELETE FROM tasks WHERE id = %s",(id,))
    cx.commit()
