from flask import Flask, request, jsonify
from deta import Deta  # Deta Base
import os

app = Flask(__name__)

# Initialize Deta Base
# If deploying via Deta Space web UI, you can leave the key blank
deta = Deta(os.environ.get("DETA_PROJECT_KEY"))  # Deta will auto-set key in Space
db = deta.Base("users")  # replaces users.json

# -----------------------
# Helper functions
# -----------------------
def get_user(username):
    return db.get(username)

def put_user(username, password, group="Normal"):
    db.put({"key": username, "password": password, "group": group})

# -----------------------
# API Endpoints
# -----------------------

# Login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username, password = data.get("username"), data.get("password")
    user = get_user(username)
    if user and user["password"] == password:
        return jsonify({"success": True})
    return jsonify({"success": False})

# Add / Update user endpoint
@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    put_user(data['username'], data['password'], data.get("group", "Normal"))
    return jsonify({"success": True})

# Change password endpoint
@app.route('/api/users/password', methods=['PUT'])
def change_password():
    data = request.json
    user = get_user(data['username'])
    if user:
        put_user(data['username'], data['password'], user.get("group", "Normal"))
        return jsonify({"success": True})
    return jsonify({"success": False})

# List all users (for admin/testing)
@app.route('/api/users', methods=['GET'])
def list_users():
    all_users = db.fetch().items  # fetch returns dict with items list
    users_sanitized = {u["key"]: {"group": u.get("group", "Normal")} for u in all_users}
    return jsonify(users_sanitized)

# -----------------------
# Run server
# -----------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5500)
