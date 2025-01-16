from flask import Flask, render_template, request, redirect, session
import os
import logging
import sys

# Configure logging first
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

try:
    app = Flask(__name__)
    
    # Get secret key from environment with fallback
    app.secret_key = os.getenv('SECRET_KEY', 'dev-key-for-testing')
    
    logger.debug("Flask app initialized")
    
    # Simple user database
    users = {
        "adminn": "password123"
    }

    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200

    @app.route('/')
    def home():
        if 'username' in session:
            return f'Welcome {session["username"]}!'
        return redirect('/login')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            if username in users and users[username] == password:
                session['username'] = username
                return redirect('/')
            return "Invalid credentials"
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        return redirect('/login')

except Exception as e:
    logger.exception("Failed to initialize application: %s", str(e))
    raise

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(host='0.0.0.0', port=5000)
