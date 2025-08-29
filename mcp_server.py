from datetime import datetime

from mcp.server.fastmcp import FastMCP

import db
from task import Task
from lecture import Lecture

mcp = FastMCP("myCalendarMCP")

db.init_db()

@mcp.tool()
def get_tasks_tool() -> list[dict]:
    """Get all tasks from the database."""
    try:
        return db.get_tasks()
    except Exception as e:
        print(f"Error getting tasks: {e}")
        return []

@mcp.tool()
def get_lectures_tool() -> list[dict]:
    """Get all lectures from the database."""
    try:
        return db.get_lectures()
    except Exception as e:
        print(f"Error getting lectures: {e}")
        return []

@mcp.tool()
def insert_task_tool(
    title: str,
    description: str,
    all_day: bool,
    start: str,
    end: str,
    status: str = "Todo"
) -> dict:
    """Insert a new task into the database.

    Args:
        title (str): The title of the task.
        description (str): The description of the task.
        all_day (bool): Whether the task is an all-day event.
        start (str): The start time in ISO format (e.g., "2025-08-26T14:30:00").
        end (str): The end time in ISO format (e.g., "2025-08-26T16:00:00").
        status (str): The status of the task, either "Todo", "In progress", or "Done" (default is "Todo").
    """

    try:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)

        if end_dt <= start_dt:
            return {"error": "End time must be after start time"}

        task = Task(
            title=title,
            description=description,
            all_day=all_day,
            start=start_dt,
            end=end_dt,
            status=status
        )

        db.insert_task(task)

        return {"message": "Task inserted successfully."}
    except Exception as e:
        return {"error": str(e)}
    
@mcp.tool()
def insert_lecture_tool(
    course: str,
    description: str,
    all_day: bool,
    start: str,
    end: str
) -> dict:
    """Insert a new lecture into the database.

    Args:
        course (str): The name of the course.
        description (str): The description of the lecture.
        all_day (bool): Whether the lecture is an all-day event.
        start (str): The start time in ISO format (e.g., "2025-08-26T14:30:00").
        end (str): The end time in ISO format (e.g., "2025-08-26T16:00:00").
    """

    try:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)

        if end_dt <= start_dt:
            return {"error": "End time must be after start time"}

        lecture = Lecture(
            course=course,
            description=description,
            all_day=all_day,
            start=start_dt,
            end=end_dt
        )      

        db.insert_lecture(lecture)

        return {"message": "Lecture inserted successfully."}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def delete_task_tool(task_id: int) -> dict:
    """Delete a task from the database by its ID.

    Args:
        task_id (int): The ID of the task to delete.

    Note:
        This action is irreversible.
        Always double-check the task ID before deleting, by retrieving the task details first.
    """
    try:
        db.delete_task(task_id)
        return {"message": "Task deleted successfully"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def delete_lecture_tool(lecture_id: int) -> dict:
    """Delete a lecture from the database by its ID.

    Args:
        lecture_id (int): The ID of the lecture to delete.

    Note:
        This action is irreversible.
        Always double-check the lecture ID before deleting, by retrieving the lecture details first.
    """
    try:
        db.delete_lecture(lecture_id)
        return {"message": "Lecture deleted successfully"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")