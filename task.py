from datetime import datetime
from typing import Any

class Task:
    def __init__(
        self,
        title: str,
        description: str,
        all_day: bool,
        start: datetime,
        end: datetime,
        status: str
    ):
        self.title = title
        self.description = description
        self.all_day = all_day
        self.start = start
        self.end = end
        self.status = status
    
    def __repr__(self) -> str:
        return f"Task(title={self.title!r}, start={self.start!r}, end={self.end!r}, status={self.status!r})"
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return (
            self.title == other.title 
            and self.start == other.start 
            and self.end == other.end
        )