# Movie Magic "Design"

**Please note that our API KEY has been changed to a local environment variable to protect it from being stolen. We got out API Key stolen after publishing it on github. So, we had to find a way to temporarily protect it by putting it in a .env file and then using .gitignore to prevent the .env file from being pushed to github.**

## Overview
Our project is a Flask-based web application designed to provide users with movie recommendations, enable them to write reviews, read reviews of others, and display trending movies. The technical implementation uses Python, Flask, JavaScript, HTML, CSS, SQL, in addition to an external TMDB [API](https://www.themoviedb.org/?language=en-US) integration and a database. The application follows a modular structure with routes handling specific functionalities, user authentication using the CS50 library, and interaction with SQL databases for storing user data and movie-related information.

## app.py
This file contains most of our backend code. It is throughly commeneted to explain what each line of code does. We modeled app.py based on what was taught in class. Functions were utilized to seperate the action of each page. For example, `def write_review():` is used to handle the operations needed to write a review along with ensuring that the data the user input is valid and can be inserted into the database.

## helpers.py
Our 'helpers.py' file was mainly designed to help render the apology (a screen returned when a user made an error: creating a password when registering that does not contain a symbol) and to handle the login required pages (ensures that a user can only access certain pages if they are logged in).

## Key Components of Our Code

### 1. Routes
The application defines various routes to handle different user interactions and functionalities. We created seperate html files for these different routes and did so as we were taught in class.

- /login: Handles user authentication through login.
- /register: Manages user registration and account creation.
- /changepassword: allows the user to change password.
- /form: Provides a form for users to specify preferences for movie recommendations.
- /trending: Fetches and displays trending movies using data from the TMDb API.
- /writereview: Enables users to write reviews for movies.
- /reviews: Displays user-generated reviews for movies.

### 2. Database Usage
Two SQL databases, `users.db` and `final_project_imdb.db`, are used in our project. `users.db` stores user authentication data, while `final_project_imdb.db` contains movie-related information (both movie information and user reviews seperated under two tables).

Here is the schema of our tables in final_project_imdb.db

```
CREATE TABLE imdb_1000GOOD (
    posterlink TEXT,
    series_title TEXT,
    release_year INT,
    certificates TEXT,
    runtime INT,
    genre TEXT,
    rating REAL,
    overview TEXT,
    metascore TEXT,
    director TEXT,
    star1 TEXT,
    star2 TEXT,
    star3 TEXT,
    star4 TEXT,
    votes TEXT,
    gross TEXT
);
CREATE TABLE MovieReviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_title VARCHAR(255) NOT NULL,
    user_rating INT NOT NULL,
    comments TEXT, time DATETIME DEFAULT CURRENT_TIMESTAMP, poster_link TEXT, username);
```

### 3. External API Integration
Our project integrates with the [TMDb API](https://www.themoviedb.org/?language=en-US) to fetch trending movies dynamically. We decided to use this API so we can provide our website users with up-to-date movie information (particularly when browsing through the current trending movies).

### 4. User Authentication
User authentication is implemented using the CS50 library, ensuring password security by hashing. The system verifies user credentials during login and securely manages user sessions. Additionally, users can change their passwords by verifying that they know the "old" password.

## Design Decisions

### 1. Code Modularity
In our project, we used a modular structure to enhance readability and maintainability. Each route handles specific functionalities, making it easier to locate and update code related to a particular feature.

### 2. Error Handling
We made sure to implement robust error handling, especially in API requests, to provide meaningful feedback to users and facilitate debugging. This ensures a smoother user experience and quick identification of issues.

### 3. User Interface (UI)
The UI is a significant component for an enhanced user experience. We incorporated Bootstrap to improve design aesthetics and responsiveness. If you want to see any of our aesthetic design choices for the website, you can check out the `styles.css` file. We decided to create a variety of classes and ids in our `styles.css` to ensure that css code would not have to be constantly copy and pasted over and over again. It would also allow one change to a class within css to quickly update across the entire site across multiple pages. This decision contributes to a visually appealing and user-friendly interface, fostering engagement amongst our users. We also added a little icon at the top of our website that appears in the tabs when you are accessing the site through google chrome or safari. The image file we used is called `apple-touch-icon.png`

### 4. Code Comments
Extensive comments have been strategically placed throughout the codebase to elucidate the flow of our thought process. 

### 5. Data Validation
Thorough input validation is implemented to prevent security vulnerabilities and improve the overall robustness of the application. It is also to ensure that the user is inputting data that we want and can work with.