# app.py
from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')

# Simple user database (in production, use a proper database)
users = {
    "adminn": "password123"
}

@app.route('/')
def home():
    if 'username' in session:
        return f'Welcome {session["username"]}!'
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            session['username'] = username
            return redirect('/')
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
