from datetime import datetime
from typing import Any

class Lecture:
    def __init__(
        self,
        course: str,
        description: str,
        all_day: bool,
        start: datetime,
        end: datetime
    ):
        self.course = course
        self.description = description
        self.all_day = all_day
        self.start = start
        self.end = end
    
    def __repr__(self) -> str:
        return f"Lectur(course={self.course!r}, start={self.start!r}, end={self.end!r})"
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Lecture):
            return NotImplemented
        return (
            self.course == other.course 
            and self.start == other.start 
            and self.end == other.end
        )