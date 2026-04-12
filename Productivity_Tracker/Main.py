import tkinter as tk
from tkinter import ttk
import Config
import Authentication
import Dashboard

class ProjectManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(Config.WINDOW_TITLE)
        self.geometry(Config.WINDOW_SIZE)
        self.current_user = None
        
        # Apply the dark background to the main window container
        self.configure(bg=Config.BG_COLOR)
        
        # Configure the global ttk style engine
        style = ttk.Style(self)
        style.theme_use('clam')
        
        # Map our dark mode colors to the default widgets
        style.configure('.', background=Config.BG_COLOR, foreground=Config.FG_COLOR, fieldbackground=Config.FRAME_BG)
        style.configure('TFrame', background=Config.BG_COLOR)
        style.configure('TLabel', background=Config.BG_COLOR, foreground=Config.FG_COLOR)
        style.configure('TButton', background=Config.FRAME_BG, foreground=Config.FG_COLOR, font=Config.FONT_NORMAL, padding=5)
        
        # Configure specific LabelFrames to blend with Dark Mode
        style.configure('TLabelframe', background=Config.BG_COLOR, foreground=Config.FG_COLOR)
        style.configure('TLabelframe.Label', background=Config.BG_COLOR, foreground=Config.FG_COLOR)
        
        # Add custom widget styles that we call throughout the app
        style.configure('Header.TLabel', font=Config.FONT_HEADER, background=Config.BG_COLOR, foreground=Config.FG_COLOR)
        style.configure('Warning.TLabel', font=Config.FONT_WARNING, background=Config.BG_COLOR, foreground='#ff6b6b')

        self.main_frame = ttk.Frame(self, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Launch exactly into the auth module
        Authentication.show_login_screen(self)

    def clear_frame(self):
        """Removes all widgets from the main frame to switch screens."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        """Points to the dashboard module"""
        Dashboard.show_dashboard(self)

if __name__ == "__main__":
    app = ProjectManagementSystem()
    app.mainloop()