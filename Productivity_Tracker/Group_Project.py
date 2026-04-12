import tkinter as tk
from tkinter import ttk, messagebox
import uuid
import Database

def show_create_group(app):
    app.clear_frame()

    ttk.Button(app.main_frame, text="← Back", command=app.show_dashboard).pack(anchor=tk.W, pady=5)
    ttk.Label(app.main_frame, text="Create Group Project", style='Header.TLabel').pack(pady=10)

    form_frame = ttk.Frame(app.main_frame)
    form_frame.pack(pady=10)

    ttk.Label(form_frame, text="Project Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
    name_var = tk.StringVar()
    ttk.Entry(form_frame, textvariable=name_var, width=30).grid(row=0, column=1, padx=10)

    ttk.Label(form_frame, text="Number of Members:").grid(row=1, column=0, sticky=tk.W, pady=5)
    count_var = tk.StringVar(value="1")
    ttk.Entry(form_frame, textvariable=count_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=10)

    members_frame = ttk.LabelFrame(app.main_frame, text="Member Usernames", padding=10)
    members_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    member_entries = []

    def generate_entries():
        for widget in members_frame.winfo_children():
            widget.destroy()
        member_entries.clear()

        try:
            count = int(count_var.get())
            if count <= 0 or count > 15:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number (1-15).")
            return

        ttk.Label(members_frame, text=f"You ({app.current_user}) are automatically the Leader.", foreground="green").pack(pady=5)
        
        for i in range(count):
            frame = ttk.Frame(members_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=f"Member {i+1} Username:").pack(side=tk.LEFT)
            var = tk.StringVar()
            ttk.Entry(frame, textvariable=var).pack(side=tk.LEFT, padx=10)
            member_entries.append(var)

    ttk.Button(form_frame, text="Set Members", command=generate_entries).grid(row=1, column=2, padx=5)

    def save_group():
        name = name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Project name is required.")
            return
        if not member_entries:
            messagebox.showerror("Error", "Please set the number of members and generate fields.")
            return

        members_dict = {}
        for var in member_entries:
            m_name = var.get().strip().lower()
            if m_name:
                if m_name == app.current_user:
                    messagebox.showwarning("Warning", f"You are already the leader, skipping '{m_name}' as member.")
                elif m_name not in Database.DB["users"]:
                    messagebox.showerror("Error", f"User '{m_name}' does not exist! They must sign up first.")
                    return
                else:
                    members_dict[m_name] = 0

        if not members_dict:
            messagebox.showerror("Error", "You must add at least one valid member.")
            return

        new_project = {
            "id": str(uuid.uuid4()),
            "name": name,
            "leader": app.current_user,
            "members": members_dict
        }
        Database.DB["group_projects"].append(new_project)
        messagebox.showinfo("Success", "Group project created successfully!")
        app.show_dashboard()

    ttk.Button(app.main_frame, text="Create Group Project", command=save_group).pack(pady=10)

def open_group_project(app, project):
    if project['leader'] == app.current_user:
        show_group_leader_window(app, project)
    else:
        show_group_member_window(app, project)

def show_group_leader_window(app, project):
    app.clear_frame()
    ttk.Button(app.main_frame, text="← Back", command=app.show_dashboard).pack(anchor=tk.W, pady=5)
    
    ttk.Label(app.main_frame, text=f"Leader View: {project['name']}", style='Header.TLabel').pack(pady=10)
    ttk.Label(app.main_frame, text="Here you can track the progress of your members' tasks.", foreground="gray").pack(pady=5)

    members_frame = ttk.Frame(app.main_frame)
    members_frame.pack(fill=tk.BOTH, expand=True, pady=20)

    for idx, (member_name, progress) in enumerate(project['members'].items()):
        row = ttk.Frame(members_frame)
        row.pack(fill=tk.X, pady=10)
        
        ttk.Label(row, text=f"@{member_name}", font=('Helvetica', 11, 'bold'), width=15).pack(side=tk.LEFT)
        pb = ttk.Progressbar(row, orient=tk.HORIZONTAL, length=300, mode='determinate')
        pb['value'] = progress
        pb.pack(side=tk.LEFT, padx=10)
        ttk.Label(row, text=f"{progress}%").pack(side=tk.LEFT)

def show_group_member_window(app, project):
    app.clear_frame()
    ttk.Button(app.main_frame, text="← Back", command=app.show_dashboard).pack(anchor=tk.W, pady=5)
    
    ttk.Label(app.main_frame, text=f"Member Task: {project['name']}", style='Header.TLabel').pack(pady=10)
    ttk.Label(app.main_frame, text=f"Leader: @{project['leader']}", foreground="gray").pack()

    frame = ttk.LabelFrame(app.main_frame, text="Update Your Task Progress (%)", padding=20)
    frame.pack(pady=30, fill=tk.X)

    current_progress = project['members'].get(app.current_user, 0)
    progress_var = tk.IntVar(value=current_progress)
    
    scale = ttk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=progress_var)
    scale.pack(fill=tk.X, pady=10)
    
    val_label = ttk.Label(frame, text=f"{current_progress}%")
    val_label.pack()

    def update_label(*args):
        val_label.config(text=f"{progress_var.get()}%")
    progress_var.trace_add('write', update_label)

    def save_member_progress():
        project['members'][app.current_user] = progress_var.get()
        messagebox.showinfo("Success", "Your task progress has been updated and sent to the leader!")
        app.show_dashboard()

    ttk.Button(frame, text="Submit Progress", command=save_member_progress).pack(pady=10)