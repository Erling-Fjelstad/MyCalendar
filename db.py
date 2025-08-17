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
                due_date TEXT, 
                status TEXT NOT NULL DEFAULT 'todo',
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(title, due_date) 
            );
        """)

def insert_task(t: Task):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO tasks (title, description, due_date, status)
            VALUES (?, ?, ?, ?)
        """, (
            t.title,
            t.description,
            t.due_date.isoformat() if isinstance(t.due_date, date) else t.due_date,
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
            due_str = row["due_date"]
            due_date = date.fromisoformat(due_str) if due_str else None
            tasks.append(Task(
                title=row["title"],
                description=row["description"],
                due_date=due_date,
                status=row["status"]
            ))

        return tasks
        