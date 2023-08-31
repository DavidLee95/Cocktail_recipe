import requests
import json
from functools import wraps
from flask import session, redirect

# Search for a particular cocktail based on the user´s input
def user_search(name):
    f = r"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=" + name
    data = requests.get(f)
    result = json.loads(data.text)
    return result

# Search for a random cocktail
def random_search():
    f = r"https://www.thecocktaildb.com/api/json/v1/1/random.php?"
    data = requests.get(f)
    result = json.loads(data.text)
    return result

# Code to ensure that the user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function