import sqlite3
from datetime import datetime

from task import Task
from lecture import Lecture
from exercise import Exercise
from project import Project


def get_connection() -> sqlite3.Connection:
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
                status TEXT NOT NULL,
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

        cur.execute("""
            CREATE TABLE IF NOT EXISTS exercises (
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

        cur.execute("""
            CREATE TABLE IF NOT EXISTS projects (
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

def insert_exercise(e: Exercise):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO exercises (course, description, all_day, start, end)
            VALUES (?, ?, ?, ?, ?)
        """, (
            e.course,
            e.description,
            e.all_day,
            e.start.isoformat() if isinstance(e.start, datetime) else e.start,
            e.end.isoformat() if isinstance(e.end, datetime) else e.end
        ))

def insert_project(p: Project):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO projects (course, description, all_day, start, end)
            VALUES (?, ?, ?, ?, ?)
        """, (
            p.course,
            p.description,
            p.all_day,
            p.start.isoformat() if isinstance(p.start, datetime) else p.start,
            p.end.isoformat() if isinstance(p.end, datetime) else p.end
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

def get_exercises() -> list[dict]:
    with get_connection() as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM exercises").fetchall()
        return [dict(r) for r in rows]

def get_projects() -> list[dict]:
    with get_connection() as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM projects").fetchall()
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
    
def get_exercises_as_objects() -> list[Exercise]:
    with get_connection() as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM exercises").fetchall()
        exercises = []

        for row in rows:
            exercises.append(Exercise(
                course=row["course"],
                description=row["description"],
                all_day=bool(row["all_day"]),
                start=datetime.fromisoformat(row["start"]),
                end=datetime.fromisoformat(row["end"])
            ))

        return exercises
    
def get_projects_as_objects() -> list[Project]:
    with get_connection() as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM projects").fetchall()
        projects = []

        for row in rows:
            projects.append(Project(
                course=row["course"],
                description=row["description"],
                all_day=bool(row["all_day"]),
                start=datetime.fromisoformat(row["start"]),
                end=datetime.fromisoformat(row["end"])
            ))

        return projects

def update_task(
    task_id: int,
    title: str,
    description: str,
    all_day: bool,
    start: str,
    end: str,
    status: str
):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE tasks
            SET title = ?, description = ?, all_day = ?, start = ?, end = ?, status = ?
            WHERE id = ?
        """, (title, description, all_day, start, end, status, task_id)
        )

def update_lecture(
    lecture_id: int,
    course: str,
    description: str,
    all_day: bool,
    start: str,
    end: str
):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE lectures
            SET course = ?, description = ?, all_day = ?, start = ?, end = ?
            WHERE id = ?
        """, (course, description, all_day, start, end, lecture_id)
        )

def update_exercise(
    exercise_id: int,
    course: str,
    description: str,
    all_day: bool,
    start: str,
    end: str
):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE exercises
            SET course = ?, description = ?, all_day = ?, start = ?, end = ?
            WHERE id = ?
        """, (course, description, all_day, start, end, exercise_id)
        )

def update_project(
    project_id: int,
    course: str,
    description: str,
    all_day: bool,
    start: str,
    end: str
):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE projects
            SET course = ?, description = ?, all_day = ?, start = ?, end = ?
            WHERE id = ?
        """, (course, description, all_day, start, end, project_id)
        )

def delete_task(task_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM tasks WHERE id = ?", 
            (task_id,)
        )

def delete_lecture(lecture_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM lectures WHERE id = ?",
            (lecture_id,)  
        )

def delete_exercise(exercise_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM exercises WHERE id = ?",
            (exercise_id,)  
        )

def delete_project(project_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM projects WHERE id = ?",
            (project_id,)
        )