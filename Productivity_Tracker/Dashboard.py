import tkinter as tk
from tkinter import ttk
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

    # Projects Lists
    lists_frame = ttk.Frame(app.main_frame)
    lists_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    # Solo List
    solo_frame = ttk.LabelFrame(lists_frame, text="Your Solo Projects", padding=10)
    solo_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
    
    # Pass config colors explicitly to Listbox
    app.solo_listbox = tk.Listbox(
        solo_frame, font=('Helvetica', 10), 
        bg=Config.FRAME_BG, fg=Config.FG_COLOR, 
        selectbackground=Config.ACCENT_COLOR, selectforeground="white",
        borderwidth=0, highlightthickness=1, highlightcolor=Config.ACCENT_COLOR
    )
    app.solo_listbox.pack(fill=tk.BOTH, expand=True)
    app.solo_listbox.bind('<Double-1>', lambda e: handle_solo_click(app))

    # Group List
    group_frame = ttk.LabelFrame(lists_frame, text="Your Group Projects", padding=10)
    group_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
    
    # Pass config colors explicitly to Listbox
    app.group_listbox = tk.Listbox(
        group_frame, font=('Helvetica', 10), 
        bg=Config.FRAME_BG, fg=Config.FG_COLOR, 
        selectbackground=Config.ACCENT_COLOR, selectforeground="white",
        borderwidth=0, highlightthickness=1, highlightcolor=Config.ACCENT_COLOR
    )
    app.group_listbox.pack(fill=tk.BOTH, expand=True)
    app.group_listbox.bind('<Double-1>', lambda e: handle_group_click(app))

    ttk.Label(app.main_frame, text="Double-click a project to open it.").pack(pady=5)
    populate_dashboard(app)

def populate_dashboard(app):
    app.solo_listbox.delete(0, tk.END)
    app.group_listbox.delete(0, tk.END)

    app.my_solo_projects = [p for p in Database.DB["solo_projects"] if p['owner'] == app.current_user]
    for p in app.my_solo_projects:
        app.solo_listbox.insert(tk.END, f"{p['name']} (Progress: {p['progress']}%)")

    app.my_group_projects = [
        p for p in Database.DB["group_projects"] 
        if p['leader'] == app.current_user or app.current_user in p['members']
    ]
    for p in app.my_group_projects:
        role = "Leader" if p['leader'] == app.current_user else "Member"
        app.group_listbox.insert(tk.END, f"{p['name']} [{role}]")

def handle_solo_click(app):
    selection = app.solo_listbox.curselection()
    if selection:
        project = app.my_solo_projects[selection[0]]
        Solo_Project.open_solo_project(app, project)

def handle_group_click(app):
    selection = app.group_listbox.curselection()
    if selection:
        project = app.my_group_projects[selection[0]]
        Group_Project.open_group_project(app, project)