# exam.py

import json
import os
import tkinter as tk
from tkinter import messagebox
from utils.email_utils import send_email
from auth import load_users, save_users

QUESTIONS_FILE = "data/questions.json"

# Load questions
def load_questions():
    if not os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "w") as f:
            json.dump([], f)
    with open(QUESTIONS_FILE, "r") as f:
        return json.load(f)

# Start the exam GUI
def start_exam(root, email):
    questions = load_questions()
    if not questions:
        messagebox.showinfo("No Questions", "No questions available. Contact admin.")
        return

    score = [0]
    current_q = [0]
    selected = tk.StringVar()

    def show_question():
        if current_q[0] < len(questions):
            q = questions[current_q[0]]
            question_label.config(text=f"{current_q[0]+1}. {q['question']}")
            selected.set(None)
            for i in range(4):
                option_buttons[i].config(text=q['options'][i], value=q['options'][i])
        else:
            finish_exam()

    def next_question():
        if selected.get() == questions[current_q[0]]['answer']:
            score[0] += 1
        current_q[0] += 1
        show_question()

    def finish_exam():
        messagebox.showinfo("Exam Finished", f"Your score: {score[0]}/{len(questions)}")
        users = load_users()
        users[email]['score'] = score[0]
        save_users(users)
        send_email(
            to=email,
            subject="Your Exam Result",
            body=f"Your score is: {score[0]} out of {len(questions)}"
        )
        root.destroy()

    for widget in root.winfo_children():
        widget.destroy()

    question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=350)
    question_label.pack(pady=20)

    option_buttons = []
    for _ in range(4):
        btn = tk.Radiobutton(root, text="", variable=selected, value="", font=("Arial", 12))
        btn.pack(anchor='w', padx=20)
        option_buttons.append(btn)

    tk.Button(root, text="Next", command=next_question).pack(pady=10)

    show_question()
