# cocktail-recipe

A website to search and save cocktail recipes!

## About cocktail-recipe:

This website allows users to search their favorite' cocktails recipe in a variety of ways. The website itself has several different pages (homepage, search, and random) by which the users can obtain the cocktail's recipes depending on whether they directly type in the name of a cocktail, click on the recommended cocktail's recipes or get randomly suggested cocktail recipes. Independently of which path the user chooses to obtain a cocktail's recipe, the final result will be displayed in another page that will contain the name, image, ingredients, and instructions to prepare the cocktail. The website itself requires the user to be logged in in order to access all the features that it offers (a registration page is also avilable), and by logging in the user can save cocktail recipes of his or her choice to view them in the future. 

Most importantly, the website makes use of the Cocktail DB API which can be found at [Cocktail DB](https://www.thecocktaildb.com/api.php). A round of applause and a special appreciation to the cocktail db's administrators for such an awesome API!

## Project files:

- flask_session: Information regarding flask's session.
- static: Where the CSS and image files are located.
- templates: Where the HTML files are located.
- app.py: The project's main python code.
- subcode.py: Where the project's sub python codes are located to be used in the app.py file.
- users.db: Where the user's login credentials and saved cocktail information are located.

### HTML page description (special thank you to [Boostrap](https://getbootstrap.com) during this section!)

- **Main menu (layout. html)**: The user can see the page's logo as well as click on 5 different menus according to his or her preference. In this page, a navbar from bootstrap was used on top so that independently of the page in which the user is lcoated, he or she may have access to the navbar all the time. In the center, the website's logo was added and to its right five options (anchor tags) were placed with different colors to direct the user to differet menus. Bootstrap's navbar was chosen because it is responsive to the screen size and its predefined functions were simple to use. On the last option, code was added so that when the user was logged in, the menu would display "Logout" and if the user was not logged in, the menu would display "Login". The rest of the space was left to use by other HTML pages.

- **Homepage (index.html)**: In this page, the user will first see a welcome message and below it find an option to search a cocktail's recipe by redirecting him or her to the search menu by using an anchor tag. On the main portion of the screen the user can find six drinks that are recommended by the website itself. Each drink has an image, name, review, and option to view the cocktail's recipe (for this a form was used with "post" as its method and redirects the user to the recipe.html page).The main portion of the page is all within a flexbox so that the content may be responsive to the screensize, and the CSS was configured for such a purpose (display: flex, flex-wrap: wrap, justify-content: space-between, align-content: space-between, width: X*vw*, height: X*vh*, etc.). CSS was used so that each of the drinks may use the same space as the others and so that the name tag, review, and the recipe option might position themselves relative to the drink image. After many different tries, this ended up being the best solution in order to maintain order and good aesthetics independently of the screen size (all text, box, image sizes adapt to the screen size).

- **Login (login.html)**: The user writes his or her credentials to login in the website. In case that the user types a username that does not exist, a flash message appears telling the user so. If the username does exist but the password is incorrect, again a flash message appears telling the user so. Instead of redirecting to the user to an error page, flash messages were used because they eliminate the need to create another "error" html page as well as they are visually more attractive. The *login* button is a form with "post" as its method that runs a python code in the app.py file. In case that the user is not registered yet, he or she can choose to do so by clicking in the bottom "Register" option, which is an anchor tag that redirects the user to the register page.

- **Register (register.html)**: This menu can only be accesed through the "Login" menu (it is not available in the navbar). In this menu, the user registers by writing a username, a password, and the password's confirmation. In case that a username is already being used, a flash message appears telling the user that the username is unavailable. In case that password and the confirmation do not match, another flash message appears telling the user that both informations do not match. The *register* button is a form with "post" as its method that runs a python code in the app.py file.

- **Recipe(recipe.html)**: When the user searches for random drinks or a specific drink, a cocktail's information (name, image, ingredients, and instructions) appears as the result by using the API provided by Cocktail DB. The information that appears is all within a flexbox that on the left has the image and on the right the ingredients and instructions within a box. CSS was used to setup this flexbox so that it would adapt the the screen size, and so that the image and information would not overlap. Once in this menu, the user can see the result provided by the website, and if he or she would like to save this drink it can be done by simply clicking on the "Save Drink" button available on the bottom of the page (this button is a form with "post" as its method). The user can later view this item in the "Saved" menu. 

- **Saved (saved.html)**: In this menu, the user can see the cocktails that he or she has saved as well as remove any cocktails that he or she does not wish to keep saved anymore. This page uses jinja in order to extract a list that it gets by getting information from the users_db. A table obtained from Bootstrap is used to display the information and has five rows in it (number, name, image, see recipe, and remove cocktail). A Bootstrap table was chosen because it makes the whole page look organized and clean. The number of columns depends on the number of cocktails saved by the user. The DB simply gives the html page the cocktail's name, and with it the page searches and displays the necessary information by principally using the Cocktail DB API. The user can click on the "Get the xxxxxx Recipe!" form (with "post" as its method) to go see the recipe to the "recipe.html" page and also clikc on the "Remove xxxxxx" form (with "post" as its method) to remove the cocktail from the DB.

- **Search (search.html)**: This menu allows the user to type the cocktail's name that the user wants to search for. In case that the user types a cocktail name that does not exist, the website flashes an error message. In case that the user does type a cocktail that exists, it redirects the user to the "recipe.html" page to display the cocktail recipe that the user is searching for. The page uses a form with a "search" input and button with "post" as its method in order to request the cocktail's search.

### App.py code description:

This is the heart of the website's functionability. It defines the logic of each one of the html pages as well as other functions such as sessions or DB. This file imports the following libraries:

```python
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from subcode import user_search, random_search, login_required #These functions will be explained on the subcode.py section!
```

The functions within the app.py file are the following:

- **def register()**: This function creates the logic behind the register.html. When the register page is loaded it simply shows the register.html; once in the page, via the "post" method that gets executed once the "Register" button is clicked, it adds the new username and password to the users.db's *users* table. However, before adding the new username and password it check the following things:

  1. The username field is not empty
  2. The password field is not empty
  3. The password confirmation field is not empty
  4. The password and confirmation fields have the same information
  5. That the username has not been used yet.
 
  In case that one of the previous conditions is not satisfied, the program sends a flash     
  message explaining which condition has not been satisfied. In case that all conditions are 
  satisfied, the program then adds the username and password (after being hashed) to the DB 
  and sends the user to the login page.

- **def index()**: The index.html page is the website's main home page. In this page, the user can perform the following actions: click on the "Search a cocktail's recipe of your choice!" to be redirected to the search.html page (anchor tag) or get the recipe of one of the six drinks that are shown ("post" method). When the user clicks on one of the recipe links, the code determines which cocktail the user chose and based on it obtains the recipe's information. Once the information is gotten, the code looks for the following information:

  1. Name
  2. Image
  3. Ingredients
  4. Instructions

  This information is sent to the recipe.html page to display the recipe to the user.
  
- **def login()**: This function handles the login logic of the login.html page. Once the user is on the login page, he or she has the option to either enter the correct credentials and login or to register. In case the user wants to register and clicks on the "register" box, he or she will be redirected to the register.html page. In case that the user wants to login, when the user clicks on the login button the code checks the following:

  1. The username field is not empty
  2. The password field is not empty
  3. The username does exist (from users.db)
  4. The password is correct (from users.db)

  In case that a condition is incorrect, a flash message will be displayed telling the user 
  which condition is incorrect. In case that all conditions are correct, the user is logged in  
  and redirected to the index.html page (home).

- **def logout()**: The logic for the logout.html page is simple. When the user clicks on the logout button, the program clears the current session and redirects the user to the index.html page(home).

- **def recipe()**: This logic controls the recipe.html page. In this page, the user can see the recipe of the cocktail that he or she chose. If the user wishes to save this recipe, he or she can simply click on the "Save Drink" button ("post" method) and add it to the saved list in the users.db file. The user is then redirected to the "saved.html" page, and a flash message appears telling the user if the cocktail was succesfully added or if previously it was already added.

- **def saved()**: This is the logic for the saved.html page. When the page is loaded, the user sees in the screen a list of his or her saved cocktail. This is achieved by obtaining from the users.db's list table the corresponding data and displaying it with the most recently added cocktial as the first one. In this page the user can do two things via the "post" method: see a drink's recipe or remove it from the saved list. When the user wants to see a drink's recipe, the program uses the user_search() function from the subcode.py file to obtain the following data which later sends it to the recipe.html page to display the result to the user:

  1. Name
  2. Image
  3. Ingredients
  4. Instructions

  If the user wants to remove a cocktail from the list, the code obtains the name of the 
  cocktail and then uses sqlite functions to remove that particular cocktail from the 
  users.db's list table. After removing the cocktail from the list, the same page is reloaded 
  but now without the removed cocktail!

- **def search()**: This function is the logic for the search.html. When the search page loads, the user sees the search.html. The page will ask the user to write the name of the cocktail that he or she wants to check. When the user writes the cocktail name and clicks on the "Search" button, the "post" method gets executed and searches for the user's cocktail through the user_search() function from the subcode.py file that uses the Cocktail DB API. The first thing that the code does is to check that the search field is not empty. In case it is, the program sends a flash message telling the user to type a cocktail name. In case that the filed is not empty, first all spaces are replaced by an underscore and then the user_search code is run to find the cocktail information. In case that there are no cocktails with that name a flash message is sent saying that the cocktail does not exist. In case it does, the code gets the information to extract the following data:

  1. Name
  2. Image
  3. Ingredients
  4. Instructions
  
  All this information is sent to the recipe.html page to display the search result to the user.

- **def random()**: This is the logic for the random.html. This function does not have a "post" method. When the user clicks on the random menu, the code uses the random_search() function from the subcode.py file in order to find random cocktail's information. Once the information is found, the code obtains the following data:

  1. Name
  2. Image
  3. Ingredients
  4. Instructions
 
  This information is sent to the recipe.html page, where the user will see the end result!

### Subcode.py code description: 

This is a sub file that has three functions that will be imported to the app.py code.

- **def user_search(name)**: The Cocktail DB provides an API in the form of a link to search for cocktails' information. In this function, the link provided by the Cocktail DB is used as a base URL, and the cocktail name that the user types (type string) is appended to the base URL to search for the specified cocktail information that the user wants to know. The function itself takes an input value "name" in the form of a string that is used to complete the URL used to search for the cocktail. The search result is given in the form of a dictionary.

- **def random_search()**: This function completely uses a link provided by the Cocktail DB to search for a random cocktail's information. Each time that the link is used, a random cocktail's information will be found. This function also gives the result in the form of a dictionary.

- **def login_required(f)**: This function ensures that the user is logged in to use certain menus in the page. In case that the user is not logged in and clicks on a certain menu that requires the user to be logged in, the function redirects the user to the login page. In this way, the function ensures that the user is logged in to access certain menus.

### Users.db code description:

This db has two tables that will be explained as the following:

- **Table: users**: This table stores a user's username and password hash. The table's id automatically increases as the number of usernames increases. This table is accesed by the register and login menus.

- **Table: list**: This table stores a user's saved cocktail's name and image based on the user's id (which is the same as the id in the users table). The table also tracks the order in which the names and images are added in order to display the most recently added cocktail on the top in the saved menu.

Thank you for taking the time to read this description!
