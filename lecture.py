from datetime import datetime

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
        return f"Course: {self.course!r} from {self.start!r} to {self.end!r}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Lecture):
            return NotImplemented
        return (
            self.course == other.course and
            self.start == other.start and
            self.end == other.end
        )