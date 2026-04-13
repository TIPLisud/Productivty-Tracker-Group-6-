import tkinter as tk
from tkinter import ttk, messagebox
import Config
import Database
import Authentication
import Solo_Project
import Group_Project

def show_dashboard(app):
    app.clear_frame()

    # Header
    header_frame = ttk.Frame(app.main_frame)
    header_frame.pack(fill=tk.X, pady=(0, 20))
    ttk.Label(header_frame, text=f"Dashboard - Welcome, {app.current_user.title()}!", style='Header.TLabel').pack(side=tk.LEFT)
    ttk.Button(header_frame, text="Sign Out", command=lambda: Authentication.show_login_screen(app)).pack(side=tk.RIGHT)

    # Action Buttons
    btn_frame = ttk.Frame(app.main_frame)
    btn_frame.pack(fill=tk.X, pady=10)
    ttk.Button(btn_frame, text="+ Create Solo Project", command=lambda: Solo_Project.show_create_solo(app)).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="+ Create Group Project", command=lambda: Group_Project.show_create_group(app)).pack(side=tk.LEFT, padx=5)

    # Projects Lists Container
    lists_frame = ttk.Frame(app.main_frame)
    lists_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    # --- SOLO PROJECTS (Listbox) ---
    solo_frame = ttk.LabelFrame(lists_frame, text="Your Solo Projects", padding=10)
    solo_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
    
    app.solo_listbox = tk.Listbox(
        solo_frame, font=('Helvetica', 10), 
        bg=Config.FRAME_BG, fg=Config.FG_COLOR, 
        selectbackground=Config.ACCENT_COLOR, selectforeground="white",
        borderwidth=0, highlightthickness=1, highlightcolor=Config.ACCENT_COLOR
    )
    app.solo_listbox.pack(fill=tk.BOTH, expand=True)
    app.solo_listbox.bind('<Double-1>', lambda e: handle_solo_click(app))

    # --- GROUP PROJECTS & INVITES (Custom Frame) ---
    group_frame = ttk.LabelFrame(lists_frame, text="Your Group Projects & Invites", padding=10)
    group_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
    
    app.group_container = tk.Frame(group_frame, bg=Config.FRAME_BG)
    app.group_container.pack(fill=tk.BOTH, expand=True)

    populate_dashboard(app)

def populate_dashboard(app):
    # 1. Populate Solo Projects
    app.solo_listbox.delete(0, tk.END)
    app.my_solo_projects = [p for p in Database.DB.get("solo_projects", []) if p['owner'] == app.current_user]
    for p in app.my_solo_projects:
        app.solo_listbox.insert(tk.END, f"{p['name']} (Progress: {p.get('progress', 0)}%)")

    # 2. Populate Group Projects & Invites
    for widget in app.group_container.winfo_children():
        widget.destroy()

    # --- SYNTAX FIX: Ensure this entire block is wrapped safely in [ ] ---
    app.my_group_projects = [
        p for p in Database.DB.get("group_projects", []) 
        if p['leader'] == app.current_user 
        or app.current_user in p.get('members', {})
        or (app.current_user in p.get('pending_invites', {}) and p['pending_invites'][app.current_user]['status'] == "Pending")
    ]
    # (If you had a print statement here, it will now work because the bracket above is closed!)

    for project in app.my_group_projects:
        # Create a row for each project
        row_frame = tk.Frame(app.group_container, bg="#2b2b2b") # Adjust bg color to match your app
        row_frame.pack(fill=tk.X, pady=4)

        is_leader = project['leader'] == app.current_user
        is_member = app.current_user in project.get('members', {})
        is_pending = app.current_user in project.get('pending_invites', {}) and project['pending_invites'][app.current_user]['status'] == "Pending"

        # --- MISSING BUTTON FIX: Re-added the ttk.Button lines! ---
        if is_leader:
            ttk.Label(row_frame, text=f"{project['name']} [Leader]", font=('Helvetica', 10, 'bold')).pack(side=tk.LEFT)
            ttk.Button(row_frame, text="Open", command=lambda p=project: Group_Project.open_group_project(app, p)).pack(side=tk.RIGHT)
        
        elif is_member:
            ttk.Label(row_frame, text=f"{project['name']} [Member]", font=('Helvetica', 10)).pack(side=tk.LEFT)
            ttk.Button(row_frame, text="Open", command=lambda p=project: Group_Project.open_group_project(app, p)).pack(side=tk.RIGHT)
        
        elif is_pending:
            ttk.Label(row_frame, text=f"🔔 {project['name']} [Invite]", font=('Helvetica', 10, 'italic'), foreground="#fcc419").pack(side=tk.LEFT)
            ttk.Button(row_frame, text="Review Invite", command=lambda p=project: Group_Project.open_group_project(app, p)).pack(side=tk.RIGHT)

def handle_solo_click(app):
    selection = app.solo_listbox.curselection()
    if selection:
        project = app.my_solo_projects[selection[0]]
        Solo_Project.open_solo_project(app, project)