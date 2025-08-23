import sqlite3
from task import Task
from lecture import Lecture
from datetime import datetime

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
                all_day INTEGER NOT NULL, 
                start TEXT NOT NULL, 
                end TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'todo',
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(title, start, end) 
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS lectures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course TEXT NOT NULL,
                description TEXT NOT NULL,
                all_day INTEGER NOT NULL, 
                start TEXT NOT NULL,
                end TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(course, start, end)
            );
        """)

def insert_task(t: Task):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO tasks (title, description, all_day, start, end, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            t.title,
            t.description,
            t.all_day,
            t.start.isoformat() if isinstance(t.start, datetime) else t.start,
            t.end.isoformat() if isinstance(t.end, datetime) else t.end,
            t.status
        ))

def insert_lecture(l: Lecture):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO lectures (course, description, all_day, start, end)
            VALUES (?, ?, ?, ?, ?)
        """, (
            l.course,
            l.description,
            l.all_day,
            l.start.isoformat() if isinstance(l.start, datetime) else l.start,
            l.end.isoformat() if isinstance(l.end, datetime) else l.end
        ))

def get_tasks() -> list[dict]:
    with get_connection() as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM tasks").fetchall()
        return [dict(r) for r in rows]
    
def get_lectures() -> list[dict]:
    with get_connection() as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM lectures").fetchall()
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
                all_day=bool(row["all_day"]),
                start=datetime.fromisoformat(row["start"]),
                end=datetime.fromisoformat(row["end"]),
                status=row["status"]
            ))

        return tasks
        

def get_lectures_as_objects() -> list[Lecture]:
    with get_connection() as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM lectures").fetchall()
        lectures = []

        for row in rows:
            lectures.append(Lecture(
                course=row["course"],
                description=row["description"],
                all_day=bool(row["all_day"]),
                start=datetime.fromisoformat(row["start"]),
                end=datetime.fromisoformat(row["end"])
            ))
        
        return lectures
