import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import uuid
import Database 

def show_create_solo(app):
    app.clear_frame()

    ttk.Button(app.main_frame, text="← Back", command=app.show_dashboard).pack(anchor=tk.W, pady=5)
    ttk.Label(app.main_frame, text="Create Solo Project", style='Header.TLabel').pack(pady=10)

    form_frame = ttk.Frame(app.main_frame)
    form_frame.pack(pady=20)

    ttk.Label(form_frame, text="Project Name:").grid(row=0, column=0, sticky=tk.W, pady=10)
    name_var = tk.StringVar()
    ttk.Entry(form_frame, textvariable=name_var, width=30).grid(row=0, column=1, padx=10)

    ttk.Label(form_frame, text="Due Date (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, pady=10)
    date_var = tk.StringVar()
    ttk.Entry(form_frame, textvariable=date_var, width=30).grid(row=1, column=1, padx=10)

    def save_solo():
        name = name_var.get().strip()
        date_str = date_var.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Project name is required.")
            return
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        new_project = {
            "id": str(uuid.uuid4()),
            "name": name,
            "due_date": date_str,
            "progress": 0,
            "owner": app.current_user
        }
        Database.DB["solo_projects"].append(new_project)
        Database.save_data() # <--- SAVES THE NEW SOLO PROJECT
        messagebox.showinfo("Success", "Solo project created successfully!")
        app.show_dashboard()

    ttk.Button(app.main_frame, text="Create Project", command=save_solo).pack(pady=20)

def open_solo_project(app, project):
    app.clear_frame()
    ttk.Button(app.main_frame, text="← Back", command=app.show_dashboard).pack(anchor=tk.W, pady=5)
    
    ttk.Label(app.main_frame, text=f"Project: {project['name']}", style='Header.TLabel').pack(pady=10)
    ttk.Label(app.main_frame, text=f"Due Date: {project['due_date']}").pack()

    try:
        due_date = datetime.strptime(project['due_date'], "%Y-%m-%d")
        today = datetime.now()
        days_left = (due_date - today).days

        if days_left < 0:
            ttk.Label(app.main_frame, text="⚠️ WARNING: THIS PROJECT IS OVERDUE!", style='Warning.TLabel').pack(pady=10)
        elif 0 <= days_left <= 3:
            ttk.Label(app.main_frame, text=f"⚠️ WARNING: Due date is very near! ({days_left} days left)", style='Warning.TLabel').pack(pady=10)
        else:
            ttk.Label(app.main_frame, text=f"Days remaining: {days_left}", foreground="green").pack(pady=10)
    except Exception:
        pass 

    frame = ttk.LabelFrame(app.main_frame, text="Update Progress (%)", padding=20)
    frame.pack(pady=20, fill=tk.X)

    progress_var = tk.IntVar(value=project['progress'])
    scale = ttk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=progress_var)
    scale.pack(fill=tk.X, pady=10)
    
    val_label = ttk.Label(frame, text=f"{project['progress']}%")
    val_label.pack()

    def update_label(*args):
        val_label.config(text=f"{progress_var.get()}%")
    progress_var.trace_add('write', update_label)

    def save_progress():
        project['progress'] = progress_var.get()
        Database.save_data() # <--- SAVES THE UPDATED PROGRESS
        messagebox.showinfo("Success", "Progress updated!")
        app.show_dashboard()

    ttk.Button(frame, text="Save Progress", command=save_progress).pack(pady=10)