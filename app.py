from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)
DATA_FILE = 'users.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE,'w') as f:
        json.dump({"Admin":{"password":"Root"}}, f)

def read_users():
    with open(DATA_FILE,'r') as f: return json.load(f)
def write_users(users):
    with open(DATA_FILE,'w') as f: json.dump(users,f)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    u, p = data.get('username'), data.get('password')
    users = read_users()
    return jsonify({"success": u in users and users[u]["password"]==p})

@app.route('/api/users', methods=['GET','POST'])
def users_api():
    users = read_users()
    if request.method=='GET': return jsonify(users)
    d=request.json; users[d['username']]={"password":d['password'],"group":d.get("group","Normal")}
    write_users(users); return jsonify({"success":True})

@app.route('/api/users/password', methods=['PUT'])
def change_password():
    data = request.json
    users = read_users()
    if data['username'] in users:
        users[data['username']]['password']=data['password']; write_users(users)
        return jsonify({"success":True})
    return jsonify({"success":False})

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5500)
