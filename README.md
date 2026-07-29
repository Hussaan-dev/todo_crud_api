# To-Do CRUD API

A small FastAPI app that manages a to-do list — create, read, update and delete tasks. Built as Week 2's assignment for the FlyRank Backend Track internship, to practice CRUD, HTTP status codes, and Swagger UI.

Data is stored in memory only — restarting the server resets it back to the 3 starter tasks. No database yet, that's next week.

## Tech Stack

- **Framework:** FastAPI
- **Validation:** Pydantic
- **Docs:** Swagger UI (built in, free with FastAPI)

## Local Setup

```bash
git clone https://github.com/Hussaan-dev/todo_crud_api.git
cd todo_crud_api
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` for the interactive Swagger UI, or hit the endpoints directly with curl.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{id}` | Get one task |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{id}` | Update a task's title and/or done status |
| DELETE | `/tasks/{id}` | Delete a task |

## Example

```bash
curl -i http://localhost:8000/tasks
```
```
HTTP/1.1 200 OK
content-type: application/json

{"tasks":[{"id":1,"title":"study","done":true},{"id":2,"title":"workout","done":false},{"id":3,"title":"meal prep","done":false}]}
```

## Swagger UI

![Swagger UI](images/swagger-docs.png)

## What I Learned

First FastAPI project. Biggest things that stuck:

- Pydantic models validate request bodies automatically — missing/wrong-type fields get rejected with a `422` before my code even runs
- Path parameters need type hints (`id: int`) or they come in as strings, which silently breaks equality checks against integer data
- `204 No Content` responses shouldn't return a body — the function just does the work and returns nothing
- Optional update fields (`str | None = None`) let a client update just one field without resending everything, but you still have to check "was this actually provided" vs "is it None by default"

## What's Left

- Query parameter filtering (`?done=true`, `?search=milk`)
- A `/stats` endpoint
- Data doesn't survive a restart — that's the point of this stage, a database comes next