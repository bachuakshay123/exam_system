# gui.py

import tkinter as tk
from tkinter import messagebox
from auth import register_user, login_user, send_otp, verify_otp
from admin import admin_login, show_admin_dashboard
from exam import start_exam

current_user = {}

def start_app():
    root = tk.Tk()
    root.title("Python Examination System")
    root.geometry("400x400")
    show_main_menu(root)
    root.mainloop()

def show_main_menu(root):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Welcome to Exam System", font=("Arial", 16)).pack(pady=10)
    tk.Button(root, text="Register", width=20, command=lambda: show_register(root)).pack(pady=5)
    tk.Button(root, text="Login", width=20, command=lambda: show_login(root)).pack(pady=5)
    tk.Button(root, text="Admin Login", width=20, command=lambda: show_admin_login(root)).pack(pady=5)

def show_register(root):
    def register():
        email = email_entry.get()
        password = password_entry.get()
        if register_user(email, password):
            send_otp(email)
            messagebox.showinfo("OTP Sent", "Check your email for OTP.")
            if verify_otp(email):
                messagebox.showinfo("Success", "Registered successfully!")
                show_main_menu(root)
            else:
                messagebox.showerror("Failed", "OTP verification failed.")
        else:
            messagebox.showerror("Error", "Email already exists.")

    clear_and_pack(root, "Register")
    email_entry, password_entry = create_login_form(root, register)

def show_login(root):
    def login():
        email = email_entry.get()
        password = password_entry.get()
        if login_user(email, password):
            current_user['email'] = email
            messagebox.showinfo("Success", "Logged in successfully!")
            start_exam(root, email)
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    clear_and_pack(root, "Login")
    email_entry, password_entry = create_login_form(root, login)

def show_admin_login(root):
    def login():
        username = username_entry.get()
        password = password_entry.get()
        if admin_login(username, password):
            show_admin_dashboard(root)
        else:
            messagebox.showerror("Error", "Invalid admin credentials.")

    clear_and_pack(root, "Admin Login")
    username_entry, password_entry = create_login_form(root, login)

def clear_and_pack(root, title):
    for widget in root.winfo_children():
        widget.destroy()
    tk.Label(root, text=title, font=("Arial", 16)).pack(pady=10)

def create_login_form(root, action_fn):
    email_label = tk.Label(root, text="Email/Username")
    email_label.pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    pass_label = tk.Label(root, text="Password")
    pass_label.pack()
    pass_entry = tk.Entry(root, show='*')
    pass_entry.pack()

    tk.Button(root, text="Submit", command=action_fn).pack(pady=10)
    return email_entry, pass_entry
