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

try:
    app = Flask(__name__)
    
    # Get secret key from environment with fallback for development
    app.secret_key = os.getenv('SECRET_KEY')
    if not app.secret_key:
        logger.warning('No SECRET_KEY set, using development key')
        app.secret_key = 'dev-key-only-for-testing'

    # Session configuration
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )

    # Simple user database (in production, use a proper database)
    users = {
        "adminn": "password123"
    }

    @app.route('/')
    def home():
        if 'username' in session:
            logger.info('User %s accessed home page', session['username'])
            return f'Welcome {session["username"]}!'
        logger.info('Redirecting unauthorized user to login')
        return redirect('/login')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            
            logger.info('Login attempt for user: %s', username)
            
            if username in users and users[username] == password:
                session['username'] = username
                logger.info('Successful login for user: %s', username)
                return redirect('/')
            
            logger.warning('Failed login attempt for user: %s', username)
            return "Invalid credentials"
        
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        username = session.get('username')
        session.clear()
        logger.info('User %s logged out', username)
        return redirect('/login')

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception('Unhandled exception: %s', str(e))
        return 'Internal Server Error', 500

except Exception as e:
    logger.exception("Failed to initialize application: %s", str(e))
    raise

# Health check endpoint
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
