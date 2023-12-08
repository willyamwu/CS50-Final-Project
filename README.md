# CS50-Final-Project

Watch our final prject video [here](https://www.youtube.com/watch?v=cR-KygAolUo)!

**Please note that our API KEY has been changed to a local environment variable to protect it from being stolen. We got out API Key stolen after publishing it on github. So, we had to find a way to temporarily protect it by putting it in a .env file and then using .gitignore to prevent the .env file from being pushed to github.**

A website that gives you recommendations on what movies to watch next.

### ACCESSING THE PROJECT

Provided in the submission is a zip file containing html, python, CSS, and SQLite database files. To access the project, unzip the file in Visual Studio Code and use “flask run” in the proper directory to access the server. You should be prompted with an http link with a format similar to this: (http://127.0.0.1:5000.).

## FEATURES

### SIGNING UP AND LOGGING IN

Upon opening the http link, you will be prompted with a login page. If you do not already have an account, click the “register” button located on the navigation bar (top right of the screen). Make sure your username is unique and that your password has numbers and symbols.

### CHANGE PASSWORD

If needed, once logged in, click “Change Password” located in the top right corner of the navigation bar. To change the password, simply enter the current password and the desired password. Then, click the blue “Change Password” button. 

### HOMEPAGE

After logging in, you will be redirected to the homepage. In addition to the navigation bar at the top of the screen, there will be two blue buttons labeled “Find a Movie!” and “Review a Movie!”. Those two buttons will take you different pages.

### MOVIE RECOMMENDATIONS

Click the blue “Find a Movie!” button to be redirected to the movie recommendation form. Here, you will see a list of checkboxes with various genres, a slider for the maximum movie length, as well as a minimum rating field. Select and adjust these options to your preference then click the blue “Submit” button located at the bottom of the form.

If needed, you can use the “Select All” button to select all preferences and maximize the maximum movie length. Or, press “Reset” if you want to change your selected preferences to the default values. These buttons are located beside the “Submit” button. 

Once you press submit, you will be prompted with ten movie recommendations accompanied by their posters, overviews, runtimes, genres, directors and release years.

At any time, press the blue “Movie Magic” logo located in the top left corner to return back to the homepage. 

### TRENDING

Press “Trending” located in the navigation bar (top of the screen) to be redirected to the trending movies page. This page live updates with the U.S.'s ten most popular movies at the current date and time by utilizing an API. Please see the note at the top regarding the API key.

### WRITE AND VIEW REVIEWS

Press “Write a Review” located in the navigation bar (top of the screen) to be redirected to a form that will allow you to write a movie review. Complete the information (title, rating, comments) and press the blue “Submit Review” button to post the review. If you type in the name of the movie incorrectly or it does not exist in the database, you will run into an apology. If you type in the title of the movie in uppercase or lowercase, the code will still be able to understand what movie you are looking for and automatically correct it for you to the correct capitalization of the movie title.

Upon pressing “submit,” you will be redirected to the movie reviews page. On the reviews page, all user-generated reviews are posted along with their corresponding posters. You are able to access the review page at any time by clicking “Reviews” located in the navigation bar. 
