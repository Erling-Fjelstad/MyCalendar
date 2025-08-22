from datetime import datetime

class Task:
    def __init__(
            self,
            title: str,
            description: str,
            start: datetime,
            end: datetime,
            status: str = "todo"
    ):
        self.title = title
        self.description = description
        self.start = start
        self.end = end
        self.status = status
    
    def __repr__(self) -> str:
        return f"Task(title = {self.title!r}, start = {self.start!r}, end = {self.end!r}, status = {self.status!r})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return (
            self.title == other.title and
            self.start == other.start and
            self.end == other.end
        )