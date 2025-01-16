from flask import Flask, render_template, request, redirect, session
import os
import logging
from logging.config import dictConfig

# Configure logging
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

app.config['DEBUG'] = True

# Secure configuration
app.secret_key = os.getenv('SECRET_KEY')
if not app.secret_key:
    raise ValueError("No SECRET_KEY set in environment variables")

# Session configuration
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=1800  # 30 minutes
)

# Simple user database (in production, use a proper database)
users = {
    "adminn": "password123"
}

@app.before_request
def log_request_info():
    app.logger.info('Headers: %s', dict(request.headers))
    app.logger.info('Method: %s, Path: %s', request.method, request.path)

@app.route('/')
def home():
    if 'username' in session:
        app.logger.info('User %s accessed home page', session['username'])
        return f'Welcome {session["username"]}!'
    app.logger.info('Redirecting unauthorized user to login')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        app.logger.info('Login attempt for user: %s', username)
        
        if username in users and users[username] == password:
            session['username'] = username
            session.permanent = True
            app.logger.info('Successful login for user: %s', username)
            return redirect('/')
        
        app.logger.warning('Failed login attempt for user: %s', username)
        return "Invalid credentials"
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    username = session.get('username')
    session.clear()
    app.logger.info('User %s logged out', username)
    return redirect('/login')

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.exception('Unhandled exception: %s', str(e))
    return 'Internal Server Error', 500

if __name__ == '__main__':
    # Development only
    app.run(host='0.0.0.0', port=5000)
