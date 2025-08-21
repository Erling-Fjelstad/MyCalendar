import sqlite3
from task import Task
from datetime import date

def get_connection():
    conn = sqlite3.connect("mycalendar.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL, 
                description TEXT NOT NULL, 
                start TEXT NOT NULL, 
                end TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'todo',
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(title, start, end) 
            );
        """)

def insert_task(t: Task):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO tasks (title, description, start, end, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            t.title,
            t.description,
            t.start.isoformat() if isinstance(t.start, date) else t.start,
            t.end.isoformat() if isinstance(t.end, date) else t.end,
            t.status
        ))

def get_tasks() -> list[dict]:
    with get_connection() as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM tasks").fetchall()
        return [dict(r) for r in rows]
    
def get_tasks_as_objects() -> list[Task]:
    with get_connection() as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM tasks").fetchall()
        tasks = []

        for row in rows:
            tasks.append(Task(
                title=row["title"],
                description=row["description"],
                start=row["start"],
                end=row["end"],
                status=row["status"]
            ))

        return tasks
        