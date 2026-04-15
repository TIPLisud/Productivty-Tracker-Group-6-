import tkinter as tk
from tkinter import ttk, messagebox
import uuid
from datetime import datetime
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

        ttk.Label(members_frame, text=f"You ({app.current_user}) are automatically the Leader.").pack(pady=5)
        
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

        pending_dict = {}
        for var in member_entries:
            m_name = var.get().strip().lower()
            if m_name:
                if m_name == app.current_user:
                    messagebox.showwarning("Warning", f"You are already the leader, skipping '{m_name}' as member.")
                elif m_name not in Database.DB["users"]:
                    messagebox.showerror("Error", f"User '{m_name}' does not exist! They must sign up first.")
                    return
                else:
                    pending_dict[m_name] = {"status": "Pending"}

        if not pending_dict:
            messagebox.showerror("Error", "You must add at least one valid member.")
            return

        new_project = {
            "id": str(uuid.uuid4()),
            "name": name,
            "leader": app.current_user,
            "members": {}, 
            "pending_invites": pending_dict, 
            "tasks": []  
        }
        
        if "group_projects" not in Database.DB:
            Database.DB["group_projects"] = []
            
        Database.DB["group_projects"].append(new_project)
        Database.save_data() # <--- SAVES THE NEW GROUP PROJECT
        messagebox.showinfo("Success", "Group project created and invites sent!")
        app.show_dashboard()

    ttk.Button(app.main_frame, text="Create Group Project", command=save_group).pack(pady=10)

# --- MAIN ROUTING LOGIC ---
def open_group_project(app, project):
    if "tasks" not in project:
        project["tasks"] = []
    if "pending_invites" not in project:
        project["pending_invites"] = {}
    if "members" not in project:
        project["members"] = {}
        
    if project['leader'] == app.current_user:
        show_group_leader_window(app, project)
    elif app.current_user in project.get("pending_invites", {}) and project["pending_invites"][app.current_user]["status"] == "Pending":
        show_invite_window(app, project) 
    else:
        show_group_member_window(app, project)

# --- DEDICATED INVITATION SCREEN ---
def show_invite_window(app, project):
    app.clear_frame()
    ttk.Button(app.main_frame, text="← Back to Dashboard", command=app.show_dashboard).pack(anchor=tk.W, pady=5)
    
    ttk.Label(app.main_frame, text="Project Invitation", style='Header.TLabel').pack(pady=10)
    ttk.Label(app.main_frame, text=f"Leader @{project['leader']} has invited you to join:", font=('Helvetica', 12)).pack(pady=5)
    ttk.Label(app.main_frame, text=f"'{project['name']}'", font=('Helvetica', 14, 'bold')).pack(pady=10)

    btn_frame = ttk.Frame(app.main_frame)
    btn_frame.pack(pady=20)

    reason_frame = ttk.Frame(app.main_frame) 

    def accept_invite():
        project["pending_invites"][app.current_user]["status"] = "Accepted"
        project["members"][app.current_user] = 0 
        Database.save_data() # <--- SAVES ACCEPTED INVITE
        messagebox.showinfo("Success", "You have officially joined the project!")
        open_group_project(app, project) 

    def show_decline_reason():
        btn_frame.pack_forget() 
        reason_frame.pack(pady=10) 

    ttk.Button(btn_frame, text="✔ Accept Invitation", command=accept_invite).pack(side=tk.LEFT, padx=10)
    ttk.Button(btn_frame, text="✖ Decline", command=show_decline_reason).pack(side=tk.LEFT, padx=10)

    ttk.Label(reason_frame, text="Please state a reason for declining:").pack(pady=5)
    reason_var = tk.StringVar()
    ttk.Entry(reason_frame, textvariable=reason_var, width=40).pack(pady=5)

    def submit_decline():
        reason = reason_var.get().strip()
        if not reason:
            messagebox.showerror("Error", "You must provide a reason to decline.")
            return
        
        project["pending_invites"][app.current_user]["status"] = "Declined"
        project["pending_invites"][app.current_user]["reason"] = reason
        Database.save_data() # <--- SAVES DECLINED INVITE
        messagebox.showinfo("Declined", "Invitation declined. The leader will see your reason.")
        app.show_dashboard()

    ttk.Button(reason_frame, text="Submit Decline", command=submit_decline).pack(pady=10)
    ttk.Button(reason_frame, text="Cancel", command=lambda: [reason_frame.pack_forget(), btn_frame.pack(pady=20)]).pack()

# --- LEADER WINDOW ---
def show_group_leader_window(app, project):
    app.clear_frame()
    ttk.Button(app.main_frame, text="← Back", command=app.show_dashboard).pack(anchor=tk.W, pady=5)
    
    ttk.Label(app.main_frame, text=f"Leader View: {project['name']}", style='Header.TLabel').pack(pady=10)

    for member_name in project['members']:
        member_tasks = [t for t in project["tasks"] if t["assignee"] == member_name]
        if member_tasks:
            done = len([t for t in member_tasks if t["status"] == "Completed"])
            project['members'][member_name] = int((done / len(member_tasks)) * 100)

    members_frame = ttk.LabelFrame(app.main_frame, text="Overall Member Progress", padding=10)
    members_frame.pack(fill=tk.X, pady=10)

    if not project['members']:
        ttk.Label(members_frame, text="No members have accepted their invites yet.", foreground="gray").pack(pady=5)
    else:
        for idx, (member_name, progress) in enumerate(project['members'].items()):
            row = ttk.Frame(members_frame)
            row.pack(fill=tk.X, pady=5)
            ttk.Label(row, text=f"@{member_name}", font=('Helvetica', 11, 'bold'), width=15).pack(side=tk.LEFT)
            pb = ttk.Progressbar(row, orient=tk.HORIZONTAL, length=200, mode='determinate')
            pb['value'] = progress
            pb.pack(side=tk.LEFT, padx=10)
            ttk.Label(row, text=f"{progress}%").pack(side=tk.LEFT)

    ttk.Separator(app.main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
    ttk.Label(app.main_frame, text="Assign Specific Tasks", style='Header.TLabel').pack(pady=5)

    task_form = ttk.Frame(app.main_frame)
    task_form.pack(pady=5)

    ttk.Label(task_form, text="Assignee:").grid(row=0, column=0, padx=5)
    assignee_var = tk.StringVar()
    member_list = list(project['members'].keys())
    assignee_cb = ttk.Combobox(task_form, textvariable=assignee_var, values=member_list, state="readonly", width=12)
    assignee_cb.grid(row=0, column=1, padx=5)

    ttk.Label(task_form, text="Task:").grid(row=0, column=2, padx=5)
    task_desc_var = tk.StringVar()
    ttk.Entry(task_form, textvariable=task_desc_var, width=20).grid(row=0, column=3, padx=5)

    ttk.Label(task_form, text="Deadline:").grid(row=0, column=4, padx=5)
    deadline_var = tk.StringVar()
    ttk.Entry(task_form, textvariable=deadline_var, width=12).grid(row=0, column=5, padx=5)

    def assign_task():
        assignee = assignee_var.get()
        desc = task_desc_var.get().strip()
        deadline = deadline_var.get().strip()

        if not assignee or not desc or not deadline:
            messagebox.showerror("Error", "All fields are required to assign a task.")
            return
        
        current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        
        project["tasks"].append({
            "id": str(uuid.uuid4()),
            "assignee": assignee,
            "description": desc,
            "deadline": deadline,
            "status": "Pending",
            "date_assigned": current_time 
        })
        Database.save_data() # <--- SAVES THE NEWLY ASSIGNED TASK
        messagebox.showinfo("Success", f"Task assigned to @{assignee}!")
        show_group_leader_window(app, project) 

    ttk.Button(task_form, text="Assign Task", command=assign_task).grid(row=0, column=6, padx=10)

    tasks_frame = ttk.LabelFrame(app.main_frame, text="Task Status Board", padding=10)
    tasks_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    if not project["tasks"]:
        ttk.Label(tasks_frame, text="No tasks assigned yet.", foreground="gray").pack()
    else:
        for task in project["tasks"]:
            status_color = "#51cf66" if task["status"] == "Completed" else "#fcc419"
            date_given = task.get("date_assigned", "Unknown")
            ttk.Label(tasks_frame, text=f"[{task['status']}] @{task['assignee']} - {task['description']} (Given: {date_given} | Due: {task['deadline']})", foreground=status_color).pack(anchor=tk.W, pady=2)

# --- MEMBER WINDOW ---
def show_group_member_window(app, project):
    app.clear_frame()
    ttk.Button(app.main_frame, text="← Back", command=app.show_dashboard).pack(anchor=tk.W, pady=5)
    
    ttk.Label(app.main_frame, text=f"Member Workspace: {project['name']}", style='Header.TLabel').pack(pady=10)
    ttk.Label(app.main_frame, text=f"Leader: @{project['leader']}").pack()

    current_user_lower = app.current_user.lower()
    my_tasks = [t for t in project["tasks"] if t.get("assignee", "").lower() == current_user_lower]
    
    if not my_tasks:
        frame = ttk.LabelFrame(app.main_frame, text="Update Your General Progress (%)", padding=15)
        frame.pack(pady=10, fill=tk.X)

        current_progress = project['members'].get(current_user_lower, project['members'].get(app.current_user, 0))
        progress_var = tk.IntVar(value=current_progress)
        
        scale = ttk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=progress_var)
        scale.pack(fill=tk.X, pady=5)
        
        val_label = ttk.Label(frame, text=f"{current_progress}%")
        val_label.pack()

        def update_label(*args):
            val_label.config(text=f"{progress_var.get()}%")
        progress_var.trace_add('write', update_label)

        def save_member_progress():
            project['members'][current_user_lower] = progress_var.get()
            Database.save_data() # <--- SAVES THE GENERAL PROGRESS UPDATES
            messagebox.showinfo("Success", "General progress updated!")
            app.show_dashboard()

        ttk.Button(frame, text="Submit Progress", command=save_member_progress).pack(pady=5)
        ttk.Label(app.main_frame, text="The leader has not assigned you any specific tasks yet.", foreground="gray").pack(pady=20)
        
    else:
        total_tasks = len(my_tasks)
        completed_tasks = len([t for t in my_tasks if t["status"] == "Completed"])
        current_progress = int((completed_tasks / total_tasks) * 100)
        
        project['members'][current_user_lower] = current_progress

        frame = ttk.LabelFrame(app.main_frame, text="Your Automated Progress", padding=15)
        frame.pack(pady=10, fill=tk.X)
        
        pb = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
        pb['value'] = current_progress
        pb.pack(pady=5)
        ttk.Label(frame, text=f"{current_progress}% (Updates automatically as you complete tasks)").pack()

        ttk.Separator(app.main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(app.main_frame, text="Your Assigned Tasks", style='Header.TLabel').pack(pady=5)

        tasks_frame = ttk.LabelFrame(app.main_frame, text="To-Do List", padding=10)
        tasks_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        for task in my_tasks:
            row = ttk.Frame(tasks_frame)
            row.pack(fill=tk.X, pady=5)
            
            date_given = task.get("date_assigned", "Unknown")
            status_text = f"[{task['status']}] {task['description']} \n(Given: {date_given}  |  Due: {task['deadline']})"
            
            if task["status"] == "Pending":
                ttk.Label(row, text=status_text, width=45).pack(side=tk.LEFT)
                
                def mark_done(t=task):
                    t["status"] = "Completed"
                    Database.save_data() # <--- SAVES COMPLETED TASK STATUS
                    messagebox.showinfo("Success", "Task completed! Progress bar updated.")
                    show_group_member_window(app, project) 

                ttk.Button(row, text="✔ Mark Done", command=mark_done).pack(side=tk.RIGHT, padx=10)
            else:
                ttk.Label(row, text=status_text, foreground="#51cf66", width=45).pack(side=tk.LEFT)
    
    total_tasks = len(my_tasks)
    if total_tasks > 0:
        completed_tasks = len([t for t in my_tasks if t["status"] == "Completed"])
        current_progress = int((completed_tasks / total_tasks) * 100)
    else:
        current_progress = project['members'].get(current_user_lower, 0)

    project['members'][current_user_lower] = current_progress
    Database.save_data() 