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
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)

    # Select all the unique symbols and sum of shares for each symbol
    rows = db.execute(
        "SELECT symbol, SUM(shares) AS shares FROM trades WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
        user_id,
    )
    # Set total net worth to cash value
    total_net_worth = user[0]["cash"]

    # Loop through the each unique symbol
    for row in rows:
        # Get the current price
        row["price"] = lookup(row["symbol"])["price"]
        # Get the value of all the holdings based on the price and shares owned
        row["total_holdings"] = row["price"] * row["shares"]
        # Add the total holdings for this symbol to the net worth
        total_net_worth += row["total_holdings"]

    # Render the page and pass through the variables
    return render_template(
        "index.html",
        username=user[0]["username"],
        cash=user[0]["cash"],
        rows=rows,
        total_net_worth=total_net_worth,
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)
        # Ensure symbol is valied
        elif lookup(request.form.get("symbol")) is None:
            return apology("invalid symbol")
        # Ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("must provide shares", 403)
        # Ensure shares are positive whole numbers
        elif request.form.get("shares").isdigit() == False:
            return apology("shares must be positive whole number")

        user_data = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        shares = int(request.form.get("shares"))
        # Gets the current stock price of the symbol
        stock_price = lookup(request.form.get("symbol"))["price"]

        # Ensure that the amount the user is trying to purchase is less than the amount of cash they have
        if stock_price * int(request.form.get("shares")) > user_data[0]["cash"]:
            return apology("too broke to afford the stock")

        # Add the trade to the trades table.
        db.execute(
            "INSERT INTO trades (user_id, symbol, shares, price, time) VALUES (:user_id, :symbol, :shares, :price, :time)",
            user_id=user_data[0]["id"],
            symbol=request.form.get("symbol"),
            shares=shares,
            price=stock_price,
            time=datetime.now(),
        )

        # Update the cash the user has.
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            user_data[0]["cash"] - (stock_price * shares),
            session["user_id"],
        )

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Get the user id of the current user
    user_id = session["user_id"]

    # Get all the trades that the user made and order it by putting the most recent at the top.
    rows = db.execute(
        "SELECT * FROM trades WHERE user_id = ? ORDER BY time DESC", user_id
    )

    # Loop through each trade
    for row in rows:
        # If the shares are positive, it represents a buy
        if row["shares"] > 0:
            row["bs"] = "Buy"
        # If the shares are megative, it represents a sell
        else:
            row["shares"] = -row["shares"]
            row["bs"] = "Sell"

    return render_template("history.html", rows=rows)


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
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")

        # Look up the symbol
        data = lookup(symbol)

        # If the function returns none, that means the symbol is not valid.
        if data is None:
            # Return this error
            return apology("Invalid symbol")

        # The symbol is valid
        else:
            return render_template("quoted.html", data=data)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)
        # Ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("must provide shares", 403)
        # Ensure shares are positive whole numbers
        elif request.form.get("shares").isdigit() == False:
            return apology("shares must be positive whole number")
        # Ensure shares being sold is less than or equal to the number of shares the individual owns
        elif int(request.form.get("shares")) > int(
            db.execute(
                "SELECT SUM(shares) AS shares FROM trades WHERE user_id = ? AND symbol = ?",
                session["user_id"],
                request.form.get("symbol"),
            )[0]["shares"]
        ):
            return apology("you are trying to sell too many shares")

        # Gather data on the current user
        user_data = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        # Gather the number of shares
        shares = int(request.form.get("shares"))

        stock_price = lookup(request.form.get("symbol"))["price"]

        # Add. the selling transaction to the trades table
        db.execute(
            "INSERT INTO trades (user_id, symbol, shares, price, time) VALUES (:user_id, :symbol, :shares, :price, :time)",
            user_id=user_data[0]["id"],
            symbol=request.form.get("symbol"),
            shares=-shares,
            price=stock_price,
            time=datetime.now(),
        )

        # Update the cash the user has
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            user_data[0]["cash"] + (stock_price * shares),
            session["user_id"],
        )

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Query database for all symbols the user owns
        rows = db.execute(
            "SELECT DISTINCT symbol FROM trades WHERE user_id = ?",
            session["user_id"],
        )
        return render_template("sell.html", rows=rows)
