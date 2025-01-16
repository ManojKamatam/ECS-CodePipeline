import os
import logging
from flask import Flask, render_template, request, redirect, session

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Initialize Flask application
app = Flask(__name__)

# Secret key for session handling
app.secret_key = os.getenv("SECRET_KEY", "default-secret-key")
logger.debug("Flask app initialized with secret key")

# Simple user database
users = {"admin": "password123"}

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

@app.route("/")
def home():
    if "username" in session:
        return f"Welcome {session['username']}!"
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["username"] = username
            logger.debug(f"User {username} logged in successfully")
            return redirect("/")
        logger.warning("Invalid login attempt")
        return "Invalid credentials", 401

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")

if __name__ == "__main__":
    logger.info("Starting Flask application")
    app.run(host="0.0.0.0", port=5000)
