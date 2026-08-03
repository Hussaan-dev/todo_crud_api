# To-Do CRUD API

A small FastAPI app that manages a to-do list — create, read, update and delete tasks. Built for the FlyRank Backend Track internship. Storage has moved three times: week 2 was an in-memory list, week 3 moved to SQLite, week 1's containerize assignment moved it again to a real Postgres database running in Docker. Same endpoints the whole way through.

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL, running in a Docker container
- **Driver:** psycopg
- **Validation:** Pydantic
- **Docs:** Swagger UI (built in)
- **Containers:** Docker + Docker Compose

## Why Postgres (and why Docker)

SQLite was fine for one file on one machine, but a real server-based database is what production backends actually use. Running it in Docker means I don't install Postgres directly — I run the official image, and it behaves the same on any machine. `docker compose up` starts the app and the database together, networked, with one command.

## Local Setup

```bash
git clone https://github.com/Hussaan-dev/todo_crud_api.git
cd todo_crud_api
cp .env.example .env
docker compose up
```

That's it — Docker builds the app image, starts Postgres, waits for it to actually be ready (via a healthcheck), then starts the API. The `tasks` table and 3 example tasks are created automatically on first run.

Visit `http://localhost:8000/docs` for the interactive Swagger UI.

### Environment variables

Set in `.env` (see `.env.example` for the required keys):

```
DATABASE_URL=postgresql://postgres:dev@localhost:5433/tasks
POSTGRES_DB=tasks
POSTGRES_USER=postgres
POSTGRES_PASSWORD=dev
```

`.env` is git-ignored — real values never get committed. `docker-compose.yml` only references `${VARIABLE}` placeholders, no secrets hardcoded in it.

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

[{"id":1,"title":"study","done":true},{"id":2,"title":"workout","done":false},{"id":3,"title":"meal prep","done":false}]
```

## Swagger UI

<img src="images/swagger-docs.png" alt="Swagger UI" width="400">

## What I Learned

- Postgres uses `%s` placeholders, not SQLite's `?` — different driver, different syntax for the same parameterized-query idea
- Postgres has no `lastrowid` — `INSERT ... RETURNING *` gets the new row back (id included) as part of the same statement
- `depends_on` alone only waits for a container to *start*, not for the database inside it to actually be ready to accept connections — needed a `healthcheck` (`pg_isready`) plus `condition: service_healthy` to fix a real race condition where the app tried to connect before Postgres had finished initializing
- Postgres 18's official image changed where it expects its volume mounted (`/var/lib/postgresql`, not `/var/lib/postgresql/data`) to make future version upgrades easier
- Inside a Compose network, containers reach each other by service name (`db`), not `localhost` — `localhost` inside a container means the container itself

## What's Left

- Query parameter filtering (`?done=true`, `?search=milk`)
- A `/stats` endpoint