class Task:
    def __init__(
            self,
            title: str,
            description: str,
            due_date: str | None = None,
            status: str = "todo"
    ):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status
    
    def __repr__(self) -> str:
        return f"Task(title = {self.title!r}, due_date = {self.due_date!r}, status = {self.status!r})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return (
            self.title == other.title and
            self.due_date == other.due_date
        )