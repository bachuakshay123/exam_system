# auth.py

import json
import os
import random
from utils.email_utils import send_email

USERS_FILE = "data/users.json"

# Load users from JSON
def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

# Save users to JSON
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Register new user
def register_user(email, password):
    users = load_users()
    if email in users:
        return False
    users[email] = {
        "password": password,
        "score": None
    }
    save_users(users)
    return True

# Login existing user
def login_user(email, password):
    users = load_users()
    return email in users and users[email]["password"] == password

# Send OTP to email
otp_map = {}

def send_otp(email):
    otp = str(random.randint(100000, 999999))
    otp_map[email] = otp
    send_email(
        to=email,
        subject="Your OTP for Exam System",
        body=f"Your OTP is: {otp}"
    )

# Verify OTP
def verify_otp(email):
    from tkinter import simpledialog
    user_input = simpledialog.askstring("OTP Verification", "Enter OTP sent to your email:")
    return user_input == otp_map.get(email)
