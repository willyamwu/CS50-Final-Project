import os
import cs50
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

# urls for APIs
trending_url = "https://api.themoviedb.org/3/trending/all/day?language=en-US"
image_url = "https://api.themoviedb.org/3/movie/movie_id/images"

# headers for API for permissions
headers = {
    "accept": "application/json",
    "Authorization": os.environ['API_KEY']
}

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")
moviesDB = SQL("sqlite:///final_project_imdb.db")


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
        preferred_length = int(request.form.get('valueSlider'))
        # preferred_decade = int(request.form.get('sliderLength'))
        rating_str = request.form.get('rating')

        # Check if a valid rating is provided
        if rating_str and rating_str.isdigit():
            rating = int(rating_str)

            # Check if any genres are selected
            genres = request.form.getlist('genre')
            if genres:
                # Create a tuple of placeholders for the genres
                genre_placeholders = ' OR '.join(
                    ['genre LIKE ?' for _ in genres])
                query = f"SELECT * FROM imdb_1000GOOD WHERE rating >= ? AND runtime <= ? AND ({genre_placeholders}) ORDER BY RANDOM() LIMIT 10"
                try:
                    # Execute the query with parameters
                    movies = moviesDB.execute(
                        query, rating, preferred_length, *["%" + genre + "%" for genre in genres])
                    return render_template("recommendation.html", movies=movies)
                except Exception as e:
                    return render_template("form.html", message=f"Error: {e}")

            # No genres selected, adjust the query accordingly
            else:
                query = "SELECT * FROM imdb_1000GOOD WHERE rating >= ? AND runtime <= ? ORDER BY RANDOM() LIMIT 10"
                try:
                    # Execute the query with parameters
                    movies = moviesDB.execute(query, rating, preferred_length)
                    return render_template("recommendation.html", movies=movies)
                except Exception as e:
                    return render_template("form.html", message=f"Error: {e}")

    # If it's a GET request or form submission failed, return the form template
    return render_template("form.html")

# Enforce the user to fill out the form in order to get recommendations.


@app.route("/recommendation", methods=["POST"])
@login_required
def recommendation():
    return redirect("/")


@app.route("/trending")
@login_required
def trending():
    # Parameters for calling the API
    params = {"language": "en-US", "page": 1}

    try:
        response = requests.get(trending_url, headers=headers, params=params)
        response.raise_for_status()  # Check for errors in the HTTP response
        data = response.json()

        # data on the 10 most popular english movies
        en_movies = [movie for movie in data.get(
            "results", []) if movie.get("original_language") == "en"][:10]

        return render_template("trending.html", movies=en_movies)

    # Return error if the API is down
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None


@app.route("/changepassword", methods=["GET", "POST"])
def change_password():
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


@app.route("/writereview", methods=["GET", "POST"])
@login_required
def write_review():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Gather user_id from the session and get the username
        user_id = session["user_id"]
        user = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        username = user[0]["username"]

        # Get the user input from the form
        movie_title = request.form.get('movieTitle')
        user_rating = int(request.form.get('rating'))
        comments = request.form.get('comments')

        # Check to see if the movie the user input exists within our database (case ignored)
        db_movie_title = moviesDB.execute(
            "SELECT series_title FROM imdb_1000GOOD WHERE series_title COLLATE NOCASE = ? LIMIT 1", movie_title)

        # If the movie does not exist, return an apology and encourage the user to try again.
        if not db_movie_title:
            return apology("Movie title was not found. Please check your spelling!", 403)

        # Add the user review into the database
        moviesDB.execute("INSERT INTO MovieReviews (movie_title, user_rating, comments, username) VALUES (?, ?, ?, ?)",
                         db_movie_title[0]["series_title"], user_rating, comments, username)

        # Select the 12 most recent reviews to display
        reviews = moviesDB.execute(
            "SELECT * FROM MovieReviews ORDER BY time DESC LIMIT 12")

        poster_links = []  # Stores all the poster links to pass through to recommendations
        for review in reviews:
            # Check to see if the movie the user input exists within our database (case ignored)
            poster_link_value = moviesDB.execute(
                "SELECT posterlink FROM imdb_1000GOOD WHERE series_title COLLATE NOCASE = ? LIMIT 1", review["movie_title"])

            try:
                # Get the poster link and append it to the list.
                poster_link = poster_link_value[0]["posterlink"]
                poster_links.append(poster_link)
            except:
                # If it does not exist, add default as a catch
                poster_links.append("Default")

        # Zip both the reviews and poster_links together to pass through to reviews.html
        return render_template("reviews.html", reviews=zip(reviews, poster_links))

    else:
        return render_template("writereview.html")


@app.route("/reviews", methods=["GET", "POST"])
@login_required
def reviews():
    # Retrieve the latest 12 reviews from the MovieReviews table, ordered by time
    reviews = moviesDB.execute(
        "SELECT * FROM MovieReviews ORDER BY time DESC LIMIT 12")

    # Initialize an empty list to store poster links for each review
    poster_links = []

    # Iterate through each review
    for review in reviews:
        # Retrieve the poster link for the corresponding movie title
        poster_link_value = moviesDB.execute(
            "SELECT posterlink FROM imdb_1000GOOD WHERE series_title COLLATE NOCASE = ? LIMIT 1", review["movie_title"])

        try:
            # Attempt to extract the poster link from the query result
            poster_link = poster_link_value[0]["posterlink"]
            poster_links.append(poster_link)
        except:
            # If an exception occurs (e.g., no poster link found), use a default value
            poster_links.append("Default")

    # Render the "reviews.html" template, passing in the reviews and corresponding poster links
    return render_template("reviews.html", reviews=zip(reviews, poster_links))