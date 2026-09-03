"""
todo_gui.py

Tkinter desktop GUI for the To-Do List application.

Run:
    python todo_gui.py

Data is stored in tasks.json (next to this file) and is shared with
the CLI version (todo_cli.py) if you run both.
"""

import tkinter as tk
from tkinter import messagebox, ttk

from todo_core import VALID_PRIORITIES, TodoManager


class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List Manager")
        self.geometry("800x540")
        self.minsize(720, 480)

        self.manager = TodoManager()

        self._build_style()
        self._build_form()
        self._build_filters()
        self._build_table()
        self._build_stats_bar()

        self.refresh_tasks()

    # ---------------------------------------------------------------
    # UI construction
    # ---------------------------------------------------------------
    def _build_style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _build_form(self) -> None:
        frame = ttk.LabelFrame(self, text="Task Details")
        frame.pack(fill="x", padx=10, pady=(10, 5))

        ttk.Label(frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.title_var, width=32).grid(
            row=0, column=1, padx=5, pady=5, sticky="w"
        )

        ttk.Label(frame, text="Priority:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.priority_var = tk.StringVar(value="Medium")
        ttk.Combobox(
            frame, textvariable=self.priority_var, values=list(VALID_PRIORITIES),
            width=10, state="readonly",
        ).grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Due date:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.due_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.due_var, width=12).grid(
            row=0, column=5, padx=5, pady=5, sticky="w"
        )
        ttk.Label(frame, text="(YYYY-MM-DD)", foreground="gray").grid(
            row=1, column=5, sticky="w", padx=5
        )

        ttk.Label(frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="ne")
        self.desc_text = tk.Text(frame, width=62, height=3)
        self.desc_text.grid(row=1, column=1, columnspan=4, padx=5, pady=5, sticky="w")

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=6, pady=(5, 8))
        ttk.Button(btn_frame, text="Add Task", command=self.add_task).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Update Selected", command=self.update_task).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).pack(side="left", padx=5)

    def _build_filters(self) -> None:
        frame = ttk.Frame(self)
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text="Filter status:").pack(side="left", padx=(0, 5))
        self.status_filter_var = tk.StringVar(value="All")
        ttk.Combobox(
            frame, textvariable=self.status_filter_var,
            values=["All", "Pending", "Completed"], width=12, state="readonly",
        ).pack(side="left", padx=5)

        ttk.Label(frame, text="Sort by:").pack(side="left", padx=(15, 5))
        self.sort_var = tk.StringVar(value="None")
        ttk.Combobox(
            frame, textvariable=self.sort_var,
            values=["None", "Priority", "Due date", "Status"], width=12, state="readonly",
        ).pack(side="left", padx=5)

        ttk.Button(frame, text="Apply", command=self.refresh_tasks).pack(side="left", padx=10)

        ttk.Button(frame, text="Delete Task", command=self.delete_task).pack(side="right", padx=5)
        ttk.Button(
            frame, text="Mark Pending", command=lambda: self.set_status("Pending")
        ).pack(side="right", padx=5)
        ttk.Button(
            frame, text="Mark Complete", command=lambda: self.set_status("Completed")
        ).pack(side="right", padx=5)

    def _build_table(self) -> None:
        columns = ("id", "title", "priority", "due", "status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        headings = {
            "id": "ID", "title": "Title", "priority": "Priority",
            "due": "Due Date", "status": "Status",
        }
        widths = {"id": 40, "title": 280, "priority": 90, "due": 100, "status": 100}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="w")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.tree.tag_configure("overdue", foreground="red")
        self.tree.tag_configure("completed", foreground="gray")

    def _build_stats_bar(self) -> None:
        self.stats_label = ttk.Label(self, text="", anchor="w")
        self.stats_label.pack(fill="x", padx=10, pady=(0, 10))

    # ---------------------------------------------------------------
    # Data operations
    # ---------------------------------------------------------------
    def refresh_tasks(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)

        status_map = {"All": None, "Pending": "Pending", "Completed": "Completed"}
        sort_map = {"None": None, "Priority": "priority", "Due date": "due_date", "Status": "status"}
        tasks = self.manager.get_all_tasks(
            status_filter=status_map.get(self.status_filter_var.get()),
            sort_by=sort_map.get(self.sort_var.get()),
        )

        for t in tasks:
            tags = []
            if t.is_overdue():
                tags.append("overdue")
            elif t.status == "Completed":
                tags.append("completed")
            self.tree.insert(
                "", "end", iid=str(t.id),
                values=(t.id, t.title, t.priority, t.due_date or "-", t.status),
                tags=tags,
            )

        stats = self.manager.get_stats()
        self.stats_label.config(
            text=(
                f"Total: {stats['total']}    Pending: {stats['pending']}    "
                f"Completed: {stats['completed']}    Overdue: {stats['overdue']}"
            )
        )

    def get_selected_id(self):
        sel = self.tree.selection()
        return int(sel[0]) if sel else None

    def on_select(self, event=None) -> None:
        task_id = self.get_selected_id()
        if task_id is None:
            return
        task = self.manager.get_task(task_id)
        if not task:
            return
        self.title_var.set(task.title)
        self.priority_var.set(task.priority)
        self.due_var.set(task.due_date or "")
        self.desc_text.delete("1.0", "end")
        self.desc_text.insert("1.0", task.description)

    def clear_form(self) -> None:
        self.title_var.set("")
        self.priority_var.set("Medium")
        self.due_var.set("")
        self.desc_text.delete("1.0", "end")
        self.tree.selection_remove(self.tree.selection())

    def add_task(self) -> None:
        title = self.title_var.get().strip()
        description = self.desc_text.get("1.0", "end").strip()
        priority = self.priority_var.get()
        due_date = self.due_var.get().strip() or None
        try:
            self.manager.add_task(title, description, priority, due_date)
            self.clear_form()
            self.refresh_tasks()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_task(self) -> None:
        task_id = self.get_selected_id()
        if task_id is None:
            messagebox.showwarning("No selection", "Select a task in the table to update.")
            return
        title = self.title_var.get().strip()
        description = self.desc_text.get("1.0", "end").strip()
        priority = self.priority_var.get()
        due_date = self.due_var.get().strip() or None
        try:
            self.manager.update_task(
                task_id, title=title, description=description,
                priority=priority, due_date=due_date,
            )
            self.refresh_tasks()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def set_status(self, status: str) -> None:
        task_id = self.get_selected_id()
        if task_id is None:
            messagebox.showwarning("No selection", "Select a task in the table first.")
            return
        if status == "Completed":
            self.manager.mark_complete(task_id)
        else:
            self.manager.mark_pending(task_id)
        self.refresh_tasks()

    def delete_task(self) -> None:
        task_id = self.get_selected_id()
        if task_id is None:
            messagebox.showwarning("No selection", "Select a task in the table first.")
            return
        if messagebox.askyesno("Confirm delete", f"Delete task #{task_id}?"):
            self.manager.delete_task(task_id)
            self.clear_form()
            self.refresh_tasks()


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
