"""
todo_cli.py

Command-line interface for the To-Do List application.

Run:
    python todo_cli.py

Data is stored in tasks.json (next to this file) and is shared with
the GUI version (todo_gui.py) if you run both.
"""

import sys

from todo_core import TodoManager, VALID_PRIORITIES

DIVIDER = "-" * 72


def print_header(title: str) -> None:
    print("\n" + DIVIDER)
    print(title)
    print(DIVIDER)


def print_tasks(tasks) -> None:
    if not tasks:
        print("No tasks found.")
        return
    header = f"{'ID':<4}{'Title':<26}{'Priority':<10}{'Due Date':<12}{'Status':<12}"
    print(header)
    print("-" * len(header))
    for t in tasks:
        flag = "  (OVERDUE)" if t.is_overdue() else ""
        title = t.title if len(t.title) <= 24 else t.title[:21] + "..."
        print(
            f"{t.id:<4}{title:<26}{t.priority:<10}"
            f"{(t.due_date or '-'):<12}{t.status:<12}{flag}"
        )


def prompt(text: str, required: bool = False) -> str:
    while True:
        raw = input(text).strip()
        if raw or not required:
            return raw
        print("This field is required.")


def choose_priority(current: str = "Medium") -> str:
    raw = input(f"Priority {VALID_PRIORITIES} [{current}]: ").strip().capitalize()
    return raw if raw in VALID_PRIORITIES else current


def add_task_flow(manager: TodoManager) -> None:
    print_header("Add New Task")
    title = prompt("Title: ", required=True)
    description = prompt("Description (optional): ")
    priority = choose_priority()
    due_date = prompt("Due date YYYY-MM-DD (optional): ")
    try:
        task = manager.add_task(title, description, priority, due_date or None)
        print(f"\n✔ Task #{task.id} added.")
    except ValueError as e:
        print(f"\n✘ Error: {e}")


def view_tasks_flow(manager: TodoManager) -> None:
    print_header("Your Tasks")
    print("Filter: 1) All   2) Pending   3) Completed")
    choice = input("Choose (Enter for All): ").strip()
    status_filter = {"2": "Pending", "3": "Completed"}.get(choice)

    sort_choice = input(
        "Sort by: 1) None   2) Priority   3) Due date   4) Status (Enter for None): "
    ).strip()
    sort_by = {"2": "priority", "3": "due_date", "4": "status"}.get(sort_choice)

    tasks = manager.get_all_tasks(status_filter=status_filter, sort_by=sort_by)
    print()
    print_tasks(tasks)


def update_task_flow(manager: TodoManager) -> None:
    print_header("Update Task")
    print_tasks(manager.get_all_tasks())
    raw_id = input("\nEnter Task ID to update (blank to cancel): ").strip()
    if not raw_id:
        return
    if not raw_id.isdigit():
        print("✘ Invalid ID.")
        return
    task = manager.get_task(int(raw_id))
    if not task:
        print("✘ Task not found.")
        return

    print("Leave a field blank to keep its current value.")
    new_title = input(f"Title [{task.title}]: ").strip()
    new_desc = input(f"Description [{task.description}]: ").strip()
    new_priority = input(f"Priority {VALID_PRIORITIES} [{task.priority}]: ").strip().capitalize()
    new_due = input(f"Due date YYYY-MM-DD [{task.due_date or '-'}]: ").strip()

    fields = {}
    if new_title:
        fields["title"] = new_title
    if new_desc:
        fields["description"] = new_desc
    if new_priority in VALID_PRIORITIES:
        fields["priority"] = new_priority
    if new_due:
        fields["due_date"] = new_due

    try:
        if manager.update_task(task.id, **fields):
            print(f"\n✔ Task #{task.id} updated.")
    except ValueError as e:
        print(f"\n✘ Error: {e}")


def toggle_status_flow(manager: TodoManager) -> None:
    print_header("Mark Task Complete / Pending")
    print_tasks(manager.get_all_tasks())
    raw_id = input("\nEnter Task ID (blank to cancel): ").strip()
    if not raw_id:
        return
    if not raw_id.isdigit():
        print("✘ Invalid ID.")
        return
    task = manager.get_task(int(raw_id))
    if not task:
        print("✘ Task not found.")
        return

    if task.status == "Pending":
        manager.mark_complete(task.id)
        print(f"\n✔ Task #{task.id} marked as Completed.")
    else:
        manager.mark_pending(task.id)
        print(f"\n✔ Task #{task.id} marked as Pending.")


def delete_task_flow(manager: TodoManager) -> None:
    print_header("Delete Task")
    print_tasks(manager.get_all_tasks())
    raw_id = input("\nEnter Task ID to delete (blank to cancel): ").strip()
    if not raw_id:
        return
    if not raw_id.isdigit():
        print("✘ Invalid ID.")
        return
    confirm = input(f"Are you sure you want to delete task #{raw_id}? (y/N): ").strip().lower()
    if confirm == "y":
        if manager.delete_task(int(raw_id)):
            print("\n✔ Task deleted.")
        else:
            print("\n✘ Task not found.")
    else:
        print("Cancelled.")


def show_stats_flow(manager: TodoManager) -> None:
    print_header("Task Statistics")
    stats = manager.get_stats()
    print(f"Total tasks:   {stats['total']}")
    print(f"Pending:       {stats['pending']}")
    print(f"Completed:     {stats['completed']}")
    print(f"Overdue:       {stats['overdue']}")


MENU = """
========== TO-DO LIST MANAGER ==========
 1. Add task
 2. View tasks
 3. Update task
 4. Mark complete / pending
 5. Delete task
 6. View statistics
 7. Exit
=========================================
"""


def main() -> None:
    manager = TodoManager()
    actions = {
        "1": add_task_flow,
        "2": view_tasks_flow,
        "3": update_task_flow,
        "4": toggle_status_flow,
        "5": delete_task_flow,
        "6": show_stats_flow,
    }
    while True:
        print(MENU)
        choice = input("Choose an option (1-7): ").strip()
        if choice == "7":
            print("Goodbye!")
            sys.exit(0)
        action = actions.get(choice)
        if action:
            action(manager)
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
