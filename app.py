from flask import Flask, request, jsonify
import os
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow Netlify frontend to call API

# Path to your JSON file
DATA_FILE = "users.json"

# -----------------------
# Helper functions
# -----------------------
def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

def get_user(username):
    users = load_users()
    return users.get(username)

def put_user(username, password, group="Normal"):
    users = load_users()
    users[username] = {"password": password, "group": group}
    save_users(users)

def remove_user(username):
    users = load_users()
    if username in users:
        del users[username]
        save_users(users)
        return True
    return False

# -----------------------
# API Endpoints
# -----------------------
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username, password = data.get("username"), data.get("password")
    user = get_user(username)
    if user and user["password"] == password:
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    put_user(data['username'], data['password'], data.get("group", "Normal"))
    return jsonify({"success": True})

@app.route('/api/users/password', methods=['PUT'])
def change_password():
    data = request.json
    user = get_user(data['username'])
    if user:
        put_user(data['username'], data['password'], user.get("group", "Normal"))
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route('/api/users', methods=['GET'])
def list_users():
    users = load_users()
    sanitized = {k: {"group": v.get("group", "Normal")} for k, v in users.items()}
    return jsonify(sanitized)

@app.route('/api/users/remove', methods=['POST'])
def remove_user_endpoint():
    data = request.json
    success = remove_user(data.get("username"))
    return jsonify({"success": success})

# -----------------------
# Run server
# -----------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
