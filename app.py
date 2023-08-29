from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from subcode import user_search, random_search, login_required

# Configure application
app = Flask(__name__)

# Ensure template are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure sessions system to not use signed cookies!
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure users db!
db = SQL("sqlite:///users.db")

# Declare global variables:
name = ""
image = ""

# This code was taken from the app.py code in the finance project!
@app.after_request
def after_request(response):
    """Ensure responses aren't cahted"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#The register menu was created and coded based on the finance project's "register.html" page and app.py!
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # Check that the user wrote a username
        if not request.form.get("username"):
            flash("Please input a username")
            return render_template("register.html")

        # Check that the user wrote a password
        elif not request.form.get("password"):
            flash("Please input a password")
            return render_template("register.html")

        # Check that the user wrote the confirmation
        elif not request.form.get("confirmation"):
            flash("Please input the confirmation")
            return render_template("register.html")

        # Check that the user's password and confirmation are the same!
        elif request.form.get("confirmation") != request.form.get("password"):
            flash("The password and the confirmation do not match")
            return render_template("register.html")

        # Check that the username has not been used yet
        elif len(db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username").lower())) == 1:
            flash("The username already exists, please choose another")
            return render_template("register.html")

        else:
            # Generate the password's hash
            hashed_password = generate_password_hash(request.form.get("password"), method="pbkdf2:sha256", salt_length=8)

            # Add username and password to DB
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username").lower(), hashed_password)

            # Send to the login page
            return render_template("login.html")
    else:
        return render_template("register.html")

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():

    if request.method == "POST":

        global name
        global image

        #Check that the user has input a cocktail name
        if not request.form.get("name"):
            flash("Please input a cocktail name")

        else:
            #Replace spaces with underscore
            user_choice = request.form.get("name").replace(' ','_')
            # Obtain the desired information from the cocktail API
            cocktail = user_search(user_choice)
            result = cocktail["drinks"]
            # Check that a result exsits
            if result == None or result[0]['strDrink'] != request.form.get("name").title():
                flash("The cocktail does not exist, please try another one!")
            else:
                name = result[0]['strDrink']
                image = result[0]['strDrinkThumb']

                #Get the desired infromation
                i = 1
                ingredients = []
                while (result[0][f'strIngredient{i}'] != None):
                    if result[0][f'strMeasure{i}'] == None:
                        measure = " "
                    else:
                        measure = result[0][f'strMeasure{i}']
                    ingredients.append(result[0][f'strIngredient{i}'] + " " + measure)
                    i += 1

                #Get the instructions
                instructions = result[0]['strInstructions']

                #Send the information to the corresponding page
                return render_template("recipe.html", name=name, image=image, ingredients=ingredients, instructions=instructions)

    return render_template("search.html")

@app.route("/saved", methods=["GET", "POST"])
@login_required
def saved():

    if request.method == "POST":

        if not request.form.get("remove"):

            global name
            global image

            # Obtain the cockail name to search
            phrase = request.form["name"]
            drink_name = phrase[8:-8]
            print(drink_name)

            # Obtain the desired information from the cocktail API
            cocktail = user_search(drink_name)
            result = cocktail["drinks"]
            name = result[0]['strDrink']
            image = result[0]['strDrinkThumb']

            # Make a list of all the ingredients and amounts
            i = 1
            ingredients = []
            while (result[0][f'strIngredient{i}'] != None):
                if result[0][f'strMeasure{i}'] == None:
                    measure = " "
                else:
                    measure = result[0][f'strMeasure{i}']
                ingredients.append(result[0][f'strIngredient{i}'] + " " + measure)
                i += 1

            #Get the instructions
            instructions = result[0]['strInstructions']
            return render_template("recipe.html", name=name, image=image, ingredients=ingredients, instructions=instructions)

        else:

            # Get the cocktail name to delete
            delete = request.form["remove"]
            drink = delete[7:]
            user_id = session["user_id"]
            db.execute("DELETE FROM list WHERE id = ? AND name = ?", user_id, drink)
            return redirect("/saved")


    # Obtain the saved list form the users.db file using the user_id
    user_id = session["user_id"]
    user_list = db.execute("SELECT name, image FROM list WHERE id = ? ORDER BY number DESC", user_id)
    #Show the main page with my information
    return render_template("saved.html", user_list = user_list)


@app.route("/random")
@login_required
def random():

    global name
    global image

    # Search for a random cocktail
    cocktail = random_search()
    result = cocktail["drinks"]
    name = result[0]['strDrink']
    image = result[0]['strDrinkThumb']


    # Make a list of all the ingredients and amounts
    i = 1
    ingredients = []
    while (result[0][f'strIngredient{i}'] != None):
        if result[0][f'strMeasure{i}'] == None:
            measure = " "
        else:
            measure = result[0][f'strMeasure{i}']
            ingredients.append(result[0][f'strIngredient{i}'] + " " + measure)
            i += 1

    #Get the instructions
    instructions = result[0]['strInstructions']

    #Send the information to the corresponding page
    return render_template("recipe.html", name=name, image=image, ingredients=ingredients, instructions=instructions)

#The login menu was created and coded based on the finance project's "login.html" page and app.py!
@app.route("/login", methods=["GET", "POST"])
def login():

    # Clear current user_id
    session.clear()

    if request.method == "POST":

        # Get the username
        username = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username").lower())

        # Check that the user wrote a username
        if not request.form.get("username"):
            flash("Please input a username")
            return render_template("login.html")

        # Check that the user wrote a password
        elif not request.form.get("password"):
            flash("Please input a password")
            return render_template("login.html")

        # Check that the username exists in the db
        elif len(username) != 1:
            flash("The username does not exist")
            return render_template("login.html")

        # Check that the password is correct
        elif not check_password_hash(username[0]["hash"], request.form.get("password")):
            flash("The password is incorrect")
            return render_template("login.html")

        # Get the user id of the logged in user
        session["user_id"] = username[0]["id"]
        return render_template("index.html")


    else:
        return render_template("login.html")

#The logout function was created and coded based on the finance project's app.py!
@app.route("/logout")
@login_required
def logout():

    # Clear user session
    session.clear()

    # Send the user to the main page
    return render_template("index.html")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        global name
        global image

        # I learned the way to obtain values from input at: https://www.codegrepper.com/search.php?answer_removed=1&q=flask%20get%20value%20of%20button
        if request.form["recipe"] == "Get the Old Fashioned Recipe!":
            cocktail_name = "old_fashioned"
        elif request.form["recipe"] == "Get the Moscow Mule Recipe!":
            cocktail_name = "moscow_mule"
        elif request.form["recipe"] == "Get the Mojito Recipe!":
            cocktail_name = "mojito"
        elif request.form["recipe"] == "Get the Whiskey Sour Recipe!":
            cocktail_name = "whiskey_sour"
        elif request.form["recipe"] == "Get the Margarita Recipe!":
            cocktail_name = "margarita"
        elif request.form["recipe"] == "Get the Manhattan Recipe!":
            cocktail_name = "manhattan"

        # Obtain the desired information from the cocktail API
        cocktail = user_search(cocktail_name)
        result = cocktail["drinks"]
        name = result[0]['strDrink']
        image = result[0]['strDrinkThumb']

        # Make a list of all the ingredients and amounts
        i = 1
        ingredients = []
        while (result[0][f'strIngredient{i}'] != None):
            if result[0][f'strMeasure{i}'] == None:
                measure = " "
            else:
                measure = result[0][f'strMeasure{i}']
            ingredients.append(result[0][f'strIngredient{i}'] + " " + measure)
            i += 1

        #Get the instructions
        instructions = result[0]['strInstructions']

        #Send the information to the corresponding page
        return render_template("recipe.html", name=name, image=image, ingredients=ingredients, instructions=instructions)

    else:
        #Show the main page with my information
        return render_template("index.html")

@app.route("/recipe", methods=["GET", "POST"])
@login_required
def recipe():

    # Add a specific drink to the user's saved list
    if request.method == 'POST':
        # Only add the drink if it has not been added yet
        if len(db.execute("SELECT * FROM list WHERE name = ?", name)) == 0:
            user_id = session["user_id"]
            db.execute("INSERT INTO list (id, name, image) VALUES (?, ?, ?)", user_id, name, image)
            flash("Cocktail added succesfully!", "success")
        else:
            flash("Cocktail was already added previously!", "error")

        return redirect("/saved")

if __name__ == "__main__":
    app.run()