# Movie Magic "Design"

**Please note that our API KEY has been changed to a local environment variable to protect it from being stolen. We got out API Key stolen after publishing it on github. So, we had to find a way to temporarily protect it.**

## Overview
Our project is a Flask-based web application designed to provide users with movie recommendations, enable them to write reviews, read reviews of others, and display trending movies. The technical implementation uses Python, Flask, JavaScript, HTML, CSS, SQL, in addition to an external [API](https://www.themoviedb.org/?language=en-US) integration and a database. The application follows a modular structure with routes handling specific functionalities, user authentication using the CS50 library, and interaction with SQL databases for storing user data and movie-related information.

## Key Components of Our Code

### 1. Routes
The application defines various routes to handle different user interactions and functionalities.

- /login: Handles user authentication through login.
- /register: Manages user registration and account creation.
- /form: Provides a form for users to specify preferences for movie recommendations.
- /trending: Fetches and displays trending movies using data from the TMDb API.
- /writereview: Enables users to write reviews for movies.
- /reviews: Displays user-generated reviews for movies.

### 2. Database Usage
Two SQL databases, `users.db` and `final_project_imdb.db`, are used in our project. `users.db` stores user authentication data, while `final_project_imdb.db` contains movie-related information (both movie information and user reviews).

### 3. External API Integration
Our project integrates with the TMDb API to fetch trending movies dynamically. We decided to use this API so we can provide our website users with up-to-date movie information (particularly when browsing through the current trending movies).

### 4. User Authentication
User authentication is implemented using the CS50 library, ensuring password security by hashing. The system verifies user credentials during login and securely manages user sessions. Additionally, users can change their passwords by verifying that they know the "old" password.

## Design Decisions

### 1. Code Modularity
In our project, we used a modular structure to enhance readability and maintainability. Each route handles specific functionalities, making it easier to locate and update code related to a particular feature.

### 2. Error Handling
We made sure to implement robust error handling, especially in API requests, to provide meaningful feedback to users and facilitate debugging. This ensures a smoother user experience and quick identification of issues.

### 3. User Interface (UI)
The UI is a significant component for an enhanced user experience. We incorporated Bootstrap, a front-end framework, to improve design aesthetics and responsiveness. This decision contributes to a visually appealing and user-friendly interface, fostering engagement amongst our users.

### 4. Code Comments
Extensive comments have been strategically placed throughout the codebase to elucidate the flow of the thought process. 

### 5. Data Validation
Thorough input validation is implemented to prevent security vulnerabilities and improve the overall robustness of the application.