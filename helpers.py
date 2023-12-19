import os
from flask import redirect, render_template, session
import datetime
from functools import wraps

def login_required(f): # f is a function, the actual one that will be done like /index or /sell, underneath
    @wraps(f) #this is a function that takes the original function and makes it keep all its metadata
    def decorated_function(*args, **kwargs): #this either makes the original function go to login or what it should be
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def apology(page, message):
    page = page + ".html"
    return render_template(page, message=message.title()) #renders the page it came from