# Stage 4 Notes — Exploring SQLite with DB Browser

Opened `tasks.db` in DB Browser for SQLite and ran a few queries directly against it, outside my API code.

**Query I ran:**
```sql
SELECT COUNT(*) FROM tasks;
```

**Result:** returned the current task count, matching exactly what `GET /tasks` showed through my API — confirming there's no "syncing" happening, DB Browser and my FastAPI app are reading and writing the exact same `tasks.db` file directly.

I also tested this live: changed a task's `done` value to `false` directly in DB Browser's "Browse Data" tab, clicked "Write Changes" to save it, then called `GET /tasks/4` through my API — it immediately reflected the new value with zero restart needed.