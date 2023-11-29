import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)

    # Render the page and pass through the variables
    return render_template(
        "index.html",
        username=user[0]["username"]
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        # Ensure that the username selected has not already been chosen
        elif db.execute(
            "SELECT * FROM users WHERE username = :username",
            username=request.form.get("username"),
        ):
            return apology("Username already exists")

        # Loop through the password to ensure that it has atleast one letter, one number, and one symbol
        symbol_found = False
        letter_found = False
        number_found = False

        for char in request.form.get("password"):
            if char.isalpha():
                letter_found = True
            elif char.isdigit():
                number_found = True
            elif not char.isalnum():
                symbol_found = True

        # Return an apology if the password does not contain at least one number, one letter, and one symbol
        if not symbol_found or not letter_found or not number_found:
            return apology("Password must contains at least one number, one letter, and one symbol")

        # Ensure the password and confirmation matches.
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match")

        # Creata hashed password and store the data into the database.
        hashed_password = generate_password_hash(request.form.get("password"))
        db.execute(
            "INSERT INTO users (username, hash) VALUES (:username, :hash)",
            username=request.form.get("username"),
            hash=hashed_password,
        )

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = :username",
            username=request.form.get("username"),
        )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/form", methods=["GET", "POST"])
@login_required
def form():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        return render_template("recommendation.html")
    return render_template("form.html")


@app.route("/recommendation", methods=["GET", "POST"])
@login_required
def recommendation():
    return render_template("recommendation.html")


@app.route("/featured", methods=["GET", "POST"])
@login_required
def featured():
    return render_template("featured.html")


@app.route("/changepassword", methods=["GET", "POST"])
def change_password():
    # Change password
    # Ensure user is submitting a password change request
    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        user_id = session["user_id"]
        # Ensure the user enters their old password
        if not old_password:
            return apology("must enter old password")
        # Ensure a new password was submitted
        if not new_password:
            return apology("must enter new password")
        # Query for old hashed password
        password_check = db.execute(
            "SELECT hash FROM users WHERE id = :user_id", user_id=user_id
        )[0]["hash"]
        # Check to ensure that the user entered the correct existing password
        if not check_password_hash(password_check, old_password):
            return apology("Incorrect password")
        # Hash the new password and upload it to the database
        hash_password = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?",
                   hash_password, user_id)
        return redirect("/")

    # User opened the webpage (no submit) and render page
    else:
        return render_template("changepassword.html")
