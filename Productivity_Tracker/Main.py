import tkinter as tk
from tkinter import ttk
import Database
import Authentication
import Solo_Project
import Group_Project

class ProjectManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Employee Project Management System")
        self.geometry("700x550")
        self.current_user = None
        
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 10), padding=5)
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
        style.configure('Warning.TLabel', font=('Helvetica', 12, 'bold'), foreground='red')

        self.main_frame = ttk.Frame(self, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Start by showing the login screen from the auth module
        Authentication.show_login_screen(self)

    def clear_frame(self):
        """Removes all widgets from the main frame to switch screens."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_frame()

        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(header_frame, text=f"Dashboard - Welcome, {self.current_user.title()}!", style='Header.TLabel').pack(side=tk.LEFT)
        ttk.Button(header_frame, text="Sign Out", command=lambda: Authentication.show_login_screen(self)).pack(side=tk.RIGHT)

        # Action Buttons
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="+ Create Solo Project", command=lambda: Solo_Project.show_create_solo(self)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="+ Create Group Project", command=lambda: Group_Project.show_create_group(self)).pack(side=tk.LEFT, padx=5)

        # Projects Lists
        lists_frame = ttk.Frame(self.main_frame)
        lists_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Solo List
        solo_frame = ttk.LabelFrame(lists_frame, text="Your Solo Projects", padding=10)
        solo_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.solo_listbox = tk.Listbox(solo_frame, font=('Helvetica', 10))
        self.solo_listbox.pack(fill=tk.BOTH, expand=True)
        self.solo_listbox.bind('<Double-1>', self.handle_solo_click)

        # Group List
        group_frame = ttk.LabelFrame(lists_frame, text="Your Group Projects", padding=10)
        group_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        self.group_listbox = tk.Listbox(group_frame, font=('Helvetica', 10))
        self.group_listbox.pack(fill=tk.BOTH, expand=True)
        self.group_listbox.bind('<Double-1>', self.handle_group_click)

        ttk.Label(self.main_frame, text="Double-click a project to open it.", foreground="gray").pack(pady=5)
        self.populate_dashboard()

    def populate_dashboard(self):
        self.solo_listbox.delete(0, tk.END)
        self.group_listbox.delete(0, tk.END)

        self.my_solo_projects = [p for p in Database.DB["solo_projects"] if p['owner'] == self.current_user]
        for p in self.my_solo_projects:
            self.solo_listbox.insert(tk.END, f"{p['name']} (Progress: {p['progress']}%)")

        self.my_group_projects = [
            p for p in Database.DB["group_projects"] 
            if p['leader'] == self.current_user or self.current_user in p['members']
        ]
        for p in self.my_group_projects:
            role = "Leader" if p['leader'] == self.current_user else "Member"
            self.group_listbox.insert(tk.END, f"{p['name']} [{role}]")

    def handle_solo_click(self, event):
        selection = self.solo_listbox.curselection()
        if selection:
            project = self.my_solo_projects[selection[0]]
            Solo_Project.open_solo_project(self, project)

    def handle_group_click(self, event):
        selection = self.group_listbox.curselection()
        if selection:
            project = self.my_group_projects[selection[0]]
            Group_Project.open_group_project(self, project)

if __name__ == "__main__":
    app = ProjectManagementSystem()
    app.mainloop()