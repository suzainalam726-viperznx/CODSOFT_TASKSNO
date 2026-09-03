# To-Do List Manager (Python)

A simple to-do list application with **both** a command-line interface and a
desktop GUI. Both share the same underlying logic and the same data file, so
you can add a task in one and see it in the other.

## Files

| File | Purpose |
|---|---|
| `todo_core.py` | Core logic: the `Task` model and `TodoManager` class (create, update, delete, list, and track tasks). Stores data in `tasks.json`. |
| `todo_cli.py` | Menu-driven command-line interface. |
| `todo_gui.py` | Tkinter desktop GUI. |
| `tasks.json` | Auto-created the first time you add a task. Holds all your tasks. |

## Requirements

- Python 3.8+
- No third-party packages needed — everything uses the standard library.
- For the GUI: Tkinter must be available. It ships with the standard
  Windows/macOS Python installers. On Linux, if you get a
  `ModuleNotFoundError: No module named 'tkinter'`, install it with:
  - Debian/Ubuntu: `sudo apt-get install python3-tk`
  - Fedora: `sudo dnf install python3-tkinter`

## Running

**Command-line version:**
```bash
python todo_cli.py
```
You'll see a numbered menu — add tasks, view/filter/sort them, update a
task's details, mark tasks complete/pending, delete tasks, or view
statistics (total, pending, completed, overdue).

**GUI version:**
```bash
python todo_gui.py
```
Fill in the form at the top and click **Add Task**. Click any row in the
table to load it into the form, edit it, and click **Update Selected**.
Use the buttons to mark a selected task complete/pending or delete it, and
use the filter/sort dropdowns above the table to change what's displayed.
A stats bar at the bottom shows your totals.

## Features

- **Create** — title (required), description, priority (High/Medium/Low),
  and an optional due date (`YYYY-MM-DD`).
- **Update** — edit any field of an existing task.
- **Track** — filter by status (Pending/Completed), sort by priority, due
  date, or status, and see live counts including how many tasks are
  overdue (shown in red in the GUI).
- **Delete** — remove tasks you no longer need, with a confirmation prompt.
- **Persistence** — tasks are saved to `tasks.json` automatically after
  every change, so nothing is lost between sessions.

## Notes on the design

`todo_core.py` has zero dependency on either front-end — it's plain Python
with no `print()` or `input()` calls — so the same logic can be reused by a
different UI, a test suite, or a future web front-end without changes.
