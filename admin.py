# admin.py

import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from auth import load_users

QUESTIONS_FILE = "data/questions.json"

# Static Admin Credentials (can also be moved to a JSON file)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def admin_login(username, password):
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

def show_admin_dashboard(root):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Admin Dashboard", font=("Arial", 16)).pack(pady=10)
    tk.Button(root, text="Add Question", width=25, command=lambda: add_question(root)).pack(pady=5)
    tk.Button(root, text="Delete Question", width=25, command=lambda: delete_question(root)).pack(pady=5)
    tk.Button(root, text="View All Questions", width=25, command=lambda: view_questions(root)).pack(pady=5)
    tk.Button(root, text="View Student Results", width=25, command=lambda: view_results(root)).pack(pady=5)
    tk.Button(root, text="Logout", width=25, command=root.destroy).pack(pady=20)

def load_questions():
    if not os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "w") as f:
            json.dump([], f)
    with open(QUESTIONS_FILE, "r") as f:
        return json.load(f)

def save_questions(questions):
    with open(QUESTIONS_FILE, "w") as f:
        json.dump(questions, f, indent=4)

def add_question(root):
    q_text = simpledialog.askstring("Add Question", "Enter question:")
    options = [simpledialog.askstring("Option", f"Enter option {i+1}:") for i in range(4)]
    answer = simpledialog.askstring("Answer", "Enter correct answer:")

    if not (q_text and all(options) and answer):
        messagebox.showerror("Error", "All fields are required.")
        return

    questions = load_questions()
    questions.append({"question": q_text, "options": options, "answer": answer})
    save_questions(questions)
    messagebox.showinfo("Success", "Question added.")

def delete_question(root):
    questions = load_questions()
    if not questions:
        messagebox.showinfo("Empty", "No questions to delete.")
        return

    index = simpledialog.askinteger("Delete Question", f"Enter question number (1-{len(questions)}):")
    if index and 1 <= index <= len(questions):
        del questions[index - 1]
        save_questions(questions)
        messagebox.showinfo("Deleted", "Question deleted successfully.")
    else:
        messagebox.showerror("Invalid", "Invalid question number.")

def view_questions(root):
    questions = load_questions()
    if not questions:
        messagebox.showinfo("Empty", "No questions found.")
        return

    top = tk.Toplevel(root)
    top.title("All Questions")
    text = tk.Text(top, wrap="word", width=60, height=20)
    text.pack()

    for idx, q in enumerate(questions, 1):
        text.insert("end", f"{idx}. {q['question']}\nOptions: {', '.join(q['options'])}\nAnswer: {q['answer']}\n\n")

def view_results(root):
    users = load_users()
    if not users:
        messagebox.showinfo("No Data", "No students registered.")
        return

    top = tk.Toplevel(root)
    top.title("Student Results")
    text = tk.Text(top, wrap="word", width=50, height=20)
    text.pack()

    for email, data in users.items():
        score = data.get("score", "Not attempted")
        text.insert("end", f"{email} - Score: {score}\n")
