
from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from functools import wraps
from urllib.parse import urlparse, urljoin
from werkzeug.security import generate_password_hash, check_password_hash
import re

login_bp = Blueprint("login", __name__)

# In-memory users store (for demo). Use a real DB in production.
USERS = {
    "hemant": generate_password_hash("1234")
}

def is_safe_url(target: str) -> bool:
    host_url = request.host_url
    ref = urlparse(host_url)
    test = urlparse(urljoin(host_url, target))
    return test.scheme in ("http", "https") and ref.netloc == test.netloc

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login.login", next=request.path))
        return view(*args, **kwargs)
    return wrapped

# Home (protected)
@login_bp.route("/")
@login_required
def home():
    return render_template("home.html")

# Register
@login_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user" in session:
        return redirect(url_for("login.home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        # Basic validation
        if not (3 <= len(username) <= 30):
            flash("Username must be 3–30 characters.", "danger")
            return redirect(url_for("login.register"))
        if not re.fullmatch(r"[a-zA-Z0-9_]+", username):
            flash("Username can contain letters, numbers and underscore only.", "danger")
            return redirect(url_for("login.register"))
        if username in USERS:
            flash("Username already taken.", "danger")
            return redirect(url_for("login.register"))
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return redirect(url_for("login.register"))
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("login.register"))

        # Save user
        USERS[username] = generate_password_hash(password)

        # Auto-login after registration
        session.clear()
        session["user"] = username
        session.permanent = True
        flash("Account created. Welcome!", "success")

        next_page = request.args.get("next")
        if next_page and is_safe_url(next_page):
            return redirect(next_page)
        return redirect(url_for("login.home"))

    return render_template("register.html")

# Login
@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("login.home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")

        password_hash = USERS.get(username)
        if password_hash and check_password_hash(password_hash, password):
            session.clear()
            session["user"] = username
            session.permanent = True
            flash("Login Successful", "success")

            next_page = request.args.get("next")
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for("login.home"))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("login.login"))

    return render_template("login.html")

# Logout
@login_bp.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for("login.login"))