from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit, join_room
import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
socketio = SocketIO(app)


DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
MESSAGES_FILE = os.path.join(DATA_DIR, 'messages.json')


os.makedirs(DATA_DIR, exist_ok=True)

# ایجاد فایل‌های JSON اگر وجود نداشته باشند
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, 'w') as f:
        json.dump([], f)

def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def load_messages():
    with open(MESSAGES_FILE, 'r') as f:
        return json.load(f)

def save_messages(messages):
    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f, indent=4)

@app.route('/')
def home():
    if 'username' in session:
        messages = load_messages()
        return render_template('index.html', username=session['username'], messages=messages)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        users = load_users()
        user = next((u for u in users if u['email'] == email), None)
        
        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='ایمیل یا رمز عبور اشتباه است')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return render_template('register.html', error='رمز عبور و تکرار آن مطابقت ندارند')
        
        users = load_users()
        
        if any(u['email'] == email for u in users):
            return render_template('register.html', error='این ایمیل قبلا ثبت شده است')
        
        if any(u['username'] == username for u in users):
            return render_template('register.html', error='این نام کاربری قبلا انتخاب شده است')
        
        hashed_password = generate_password_hash(password)
        new_user = {
            'username': username,
            'email': email,
            'password': hashed_password
        }
        
        users.append(new_user)
        save_users(users)
        
        session['username'] = username
        return redirect(url_for('home'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@socketio.on('send_message')
def handle_send_message(data):
    if 'username' not in session:
        return
    
    message = {
        'username': session['username'],
        'text': data['message'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    messages = load_messages()
    messages.append(message)
    save_messages(messages)
    
    emit('receive_message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
