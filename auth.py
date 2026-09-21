import json
import os
import hashlib

DB_FILE = "dbase.json"

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(login, password):
    users = load_users()
    if login in users:
        return False, "user already exists"
    users[login] = hash_password(password)
    save_users(users)
    return True, "registration successful"

def login(login, password):
    users = load_users()
    if login in users and users[login] == hash_password(password):
        return True, "login successful"
    return False, "invalid login or password"
