import tkinter as tk
from tkinter import ttk, messagebox
import Database

def show_login_screen(app):
    app.clear_frame()
    app.current_user = None

    ttk.Label(app.main_frame, text="System Sign In", style='Header.TLabel').pack(pady=(50, 20))
    
    ttk.Label(app.main_frame, text="Username:").pack(pady=(10, 2))
    username_var = tk.StringVar()
    ttk.Entry(app.main_frame, textvariable=username_var, font=('Helvetica', 12)).pack(pady=5)

    ttk.Label(app.main_frame, text="Password:").pack(pady=(10, 2))
    password_var = tk.StringVar()
    ttk.Entry(app.main_frame, textvariable=password_var, font=('Helvetica', 12), show="*").pack(pady=5)

    def attempt_login():
        user = username_var.get().strip().lower()
        password = password_var.get()
        
        if not user or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        if user in Database.DB["users"] and Database.DB["users"][user] == password:
            app.current_user = user
            app.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    ttk.Button(app.main_frame, text="Sign In", command=attempt_login).pack(pady=20)
    
    ttk.Label(app.main_frame, text="Don't have an account?").pack(pady=(20, 5))
    ttk.Button(app.main_frame, text="Sign Up Here", command=lambda: show_signup_screen(app)).pack()

def show_signup_screen(app):
    app.clear_frame()

    ttk.Button(app.main_frame, text="← Back to Sign In", command=lambda: show_login_screen(app)).pack(anchor=tk.W, pady=5)
    ttk.Label(app.main_frame, text="Create an Account", style='Header.TLabel').pack(pady=(10, 20))
    
    ttk.Label(app.main_frame, text="Choose a Username:").pack(pady=(5, 2))
    username_var = tk.StringVar()
    ttk.Entry(app.main_frame, textvariable=username_var, font=('Helvetica', 12)).pack(pady=5)

    ttk.Label(app.main_frame, text="Create a Password:").pack(pady=(10, 2))
    password_var = tk.StringVar()
    ttk.Entry(app.main_frame, textvariable=password_var, font=('Helvetica', 12), show="*").pack(pady=5)

    ttk.Label(app.main_frame, text="Confirm Password:").pack(pady=(10, 2))
    confirm_password_var = tk.StringVar()
    ttk.Entry(app.main_frame, textvariable=confirm_password_var, font=('Helvetica', 12), show="*").pack(pady=5)

    def attempt_signup():
        user = username_var.get().strip().lower()
        password = password_var.get()
        confirm = confirm_password_var.get()
        
        if not user or not password:
            messagebox.showerror("Error", "All fields are required.")
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        if user in Database.DB["users"]:
            messagebox.showerror("Error", "Username already exists.")
            return

        Database.DB["users"][user] = password
        messagebox.showinfo("Success", f"Account created for '{user}'! You can now sign in.")
        show_login_screen(app)

    ttk.Button(app.main_frame, text="Sign Up", command=attempt_signup).pack(pady=20)