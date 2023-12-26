import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology, datetime, get_question_and_answers, get_ideas, expand_idea
from openai import OpenAI
import secrets

client = OpenAI()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = secrets.token_hex(16)

db = SQL("sqlite:///db.db")

# Fixed Expand and Save buttons

QUESTIONS_BEFORE_IDEAS = 5

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
# @login_required
def quiz():
    if request.method == "POST":
        # add selected option to selections session data
        selected_option = request.form.get("option")
        selections = session["quiz_selections"]
        selections[-1] = {"question": selections[-1]["question"], "answer": selected_option, "options": selections[-1]["options"]}

        session["quiz_selections"] = selections

        if len(selections) >= QUESTIONS_BEFORE_IDEAS:
            ideas = get_ideas(selections, client)
            return render_template("quiz.html", current_selection=None, previous_selections= reversed(selections), ideas=ideas, has_ideas=True)
    else:
        session["quiz_selections"] = []  # dicts with format {question, answer} - set to empty everytime start quiz (GET page)

    question, options = get_question_and_answers(session["quiz_selections"], client)
    session["quiz_selections"].append({"question": question, "options": options})

    return render_template("quiz.html", current_selection=session["quiz_selections"][-1],previous_selections=reversed(session["quiz_selections"][:-1]), has_ideas=False)

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology('register', "Username entry is required")
        elif not password:
            return apology('register', "Password entry is required")
        elif password != confirmation:
            return apology('register', "Password and confirmation do not match")
        elif db.execute("SELECT username FROM users WHERE username = ?", username):
            return apology('register', "Username in use")

        elif len(password) < 8:
            return apology('register', "password must be at least 8 characters")
        elif not re.search(r'[A-Z]', password):
            return apology('register', "password must contain a capital letter")
        elif not re.search(r'[a-z]', password):
            return apology('register', "password must contain a lowercase letter")
        elif not re.search(r'\d', password):
            return apology('register', "password must contain a digit")

        db.execute("INSERT INTO users(username, hash, date_created) VALUES(?, ?, ?)",
            username, generate_password_hash(password), datetime.datetime.now())
        session["user_id"] = db.execute(
            "SELECT userID FROM users WHERE username = ?", username)
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
            return apology('login', "Username entry is required")

        if not password:
            return apology('login', "Password entry is required")

        user = db.execute(
            "SELECT userID, username, hash FROM users WHERE username = ?", username)

        if not user or not check_password_hash(user[0]["hash"], password):
            return apology('login', "Invalid username/ password")
        session["user_id"] = user[0]["userID"]
        return redirect("/")
    else:
        return render_template("login.html")



@app.route("/expand", methods=["GET", "POST"])
@login_required
def expand():
    if not request.form.__contains__("idea"):
        return render_template("error.html", header="400", message="User did not provide an idea string to page or was in invalid correct form")

    idea = request.form.get("idea")
    expansion, similars = expand_idea(idea, client)
    return render_template("expand.html", idea=idea, expansion=expansion, similar_ideas=similars)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", header="404", message="Page not found")