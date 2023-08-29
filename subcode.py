import requests
import json
from functools import wraps
from flask import session, redirect

# The method to get the cocktail information from the API was obtained from: https://holypython.com/api-12-cocktail-database/
def user_search(name):
    f = r"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=" + name
    data = requests.get(f)
    result = json.loads(data.text)
    return result

def random_search():
    f = r"https://www.thecocktaildb.com/api/json/v1/1/random.php?"
    data = requests.get(f)
    result = json.loads(data.text)
    return result

# This code was obtained from https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/ and from the finance project's helpers.py code
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function