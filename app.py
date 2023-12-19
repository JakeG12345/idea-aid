import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
# from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology, datetime, get_question_and_answers
from openai import OpenAI

client = OpenAI()

app = Flask(__name__)

db = SQL("sqlite:///db.db")

@app.route("/")
@login_required
def index():
    # print(completion.choices[0].message)

    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        selection = request.form.get("option")
        print("User selected option:", selection)
        session["quiz_selections"][-1]["answer"] = selection
    else:
        session["quiz_selections"] = [] # dicts with format {question, answer}

    content = get_question_and_answers(session["quiz_selections"], client)
    
    question, optionsD = content.split("::")
    session["quiz_selections"].append({"question": question})
    options = optionsD.split(",")

    print("Quiz selections:", session["quiz_selections"])

    return render_template("quiz.html", question=question, options=options)

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology(__name__, "Username entry is required")
        elif not password:
            return apology(__name__, "Password entry is required")
        elif password != confirmation:
            return apology(__name__, "Password and confirmation do not match")
        elif db.execute("SELECT username FROM users WHERE username = ?", username):
            return apology(__name__, "Username in use")
        # elif username: will have password conditions here (legth, numbers)
        #     return apology(__name__, "")
        else:
            db.execute("INSERT INTO users (username, hash, date_created) VALUES(?, ?, ?)", username, generate_password_hash(password), datetime.datetime.now())
            session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", username)
            return redirect("/")

    else:
        return render_template("register.html")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return apology(__name__, "Username entry is required")
        elif not password:
            return apology(__name__, "Password entry is required")
        elif username in db.execute("SELECT username FROM users"):
            return apology(__name__, "Username entry is required")
        
        user = db.execute("SELECT username, hash FROM users")
        if not user:
            return apology(__name__, "Invalid username")
        elif check_password_hash(user[0]["hash"], password):
            return apology(__name__, "Invalid username")
        session["user_id"] = user[0]["id"]

        return redirect("/")
    else:
        return render_template("login.html")