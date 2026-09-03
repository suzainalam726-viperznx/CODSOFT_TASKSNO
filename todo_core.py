"""
todo_core.py

Core data model and storage logic for the To-Do List application.
This module is shared by both front-ends:
  - todo_cli.py  (command-line interface)
  - todo_gui.py  (Tkinter GUI)

It has no dependency on either front-end, so it can also be imported
and reused in tests or other tools.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional

VALID_PRIORITIES = ("High", "Medium", "Low")
VALID_STATUSES = ("Pending", "Completed")

# Tasks are persisted next to this file by default, so both the CLI and
# GUI front-ends share the same data automatically.
DEFAULT_DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "tasks.json"
)


@dataclass
class Task:
    """A single to-do item."""

    id: int
    title: str
    description: str = ""
    priority: str = "Medium"          # High / Medium / Low
    due_date: Optional[str] = None    # "YYYY-MM-DD"
    status: str = "Pending"           # Pending / Completed
    created_at: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Task":
        return Task(**data)

    def is_overdue(self) -> bool:
        """A task is overdue if it has a due date in the past and isn't done."""
        if not self.due_date or self.status == "Completed":
            return False
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d").date()
        except ValueError:
            return False
        return due < datetime.now().date()


class TodoManager:
    """Handles all CRUD operations and JSON persistence for tasks."""

    def __init__(self, filepath: str = DEFAULT_DATA_FILE):
        self.filepath = filepath
        self.tasks: List[Task] = []
        self._next_id = 1
        self.load()

    # ---------------------------------------------------------------
    # Persistence
    # ---------------------------------------------------------------
    def load(self) -> None:
        """Load tasks from the JSON file, if it exists."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                self.tasks = [Task.from_dict(t) for t in raw]
                if self.tasks:
                    self._next_id = max(t.id for t in self.tasks) + 1
            except (json.JSONDecodeError, TypeError, KeyError):
                # Corrupt or unreadable file: start fresh rather than crash.
                self.tasks = []
        else:
            self.tasks = []

    def save(self) -> None:
        """Write the current task list to the JSON file."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    # ---------------------------------------------------------------
    # Create / Read / Update / Delete
    # ---------------------------------------------------------------
    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "Medium",
        due_date: Optional[str] = None,
    ) -> Task:
        title = (title or "").strip()
        if not title:
            raise ValueError("Title cannot be empty.")
        priority = priority if priority in VALID_PRIORITIES else "Medium"
        if due_date:
            self._validate_date(due_date)

        task = Task(
            id=self._next_id,
            title=title,
            description=(description or "").strip(),
            priority=priority,
            due_date=due_date or None,
        )
        self.tasks.append(task)
        self._next_id += 1
        self.save()
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        return next((t for t in self.tasks if t.id == task_id), None)

    def update_task(self, task_id: int, **fields: Any) -> bool:
        """Update one or more fields of a task. Unknown/blank fields are ignored."""
        task = self.get_task(task_id)
        if not task:
            return False

        if fields.get("title"):
            task.title = fields["title"].strip()
        if fields.get("description") is not None:
            task.description = fields["description"].strip()
        if fields.get("priority") in VALID_PRIORITIES:
            task.priority = fields["priority"]
        if "due_date" in fields:
            due = fields["due_date"]
            if due:
                self._validate_date(due)
            task.due_date = due or None
        if fields.get("status") in VALID_STATUSES:
            task.status = fields["status"]

        self.save()
        return True

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
        self.tasks.remove(task)
        self.save()
        return True

    def mark_complete(self, task_id: int) -> bool:
        return self.update_task(task_id, status="Completed")

    def mark_pending(self, task_id: int) -> bool:
        return self.update_task(task_id, status="Pending")

    # ---------------------------------------------------------------
    # Querying / tracking
    # ---------------------------------------------------------------
    def get_all_tasks(
        self,
        status_filter: Optional[str] = None,
        priority_filter: Optional[str] = None,
        sort_by: Optional[str] = None,
    ) -> List[Task]:
        result = list(self.tasks)

        if status_filter and status_filter in VALID_STATUSES:
            result = [t for t in result if t.status == status_filter]
        if priority_filter and priority_filter in VALID_PRIORITIES:
            result = [t for t in result if t.priority == priority_filter]

        if sort_by == "priority":
            order = {"High": 0, "Medium": 1, "Low": 2}
            result.sort(key=lambda t: order.get(t.priority, 1))
        elif sort_by == "due_date":
            result.sort(key=lambda t: (t.due_date is None, t.due_date or ""))
        elif sort_by == "status":
            result.sort(key=lambda t: t.status)

        return result

    def get_stats(self) -> Dict[str, int]:
        """Simple counts used to 'track' overall to-do list progress."""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.status == "Completed")
        pending = total - completed
        overdue = sum(1 for t in self.tasks if t.is_overdue())
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "overdue": overdue,
        }

    # ---------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------
    @staticmethod
    def _validate_date(date_str: str) -> None:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date '{date_str}'. Use format YYYY-MM-DD.")
