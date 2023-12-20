import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
# from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology, datetime, get_question_and_answers, get_ideas
from openai import OpenAI
import secrets

client = OpenAI()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = secrets.token_hex(16)

db = SQL("sqlite:///db.db")

QUESTIONS_BEFORE_IDEAS = 8

@app.route("/")
@login_required
def index():
    print(session["user_id"])
    # print(completion.choices[0].message)
    return redirect("/quiz")
    # return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        selection = request.form.get("option")
        print("User selected option:", selection)
        selections = session["quiz_selections"]
        selections[-1] = { "question": selections[-1]["question"], "answer": selection }
        session["quiz_selections"] = selections

        if len(selections) >= QUESTIONS_BEFORE_IDEAS:
            return redirect("/ideas")
    else:
        print("RESET QUIZ SELECTIONS")
        session["quiz_selections"] = []  # dicts with format {question, answer}

    print("Quiz selections (a):", session["quiz_selections"], len(session["quiz_selections"]))

    content = get_question_and_answers(session["quiz_selections"], client)

    question, optionsD = content.split("::")
    session["quiz_selections"].append({"question": question })
    options = optionsD.split(",")

    print("Quiz selections (b):", session["quiz_selections"], len(session["quiz_selections"]))

    return render_template("quiz.html", question=question, options=options)


@app.route("/ideas", methods=["GET"])
def ideas():
    ideas = get_ideas(session["quiz_selections"], client)
    return render_template("ideas.html", ideas=ideas)

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
             return apology('index', "Username entry is required")
        elif not password:
            return apology('index', "Password entry is required")
        elif password != confirmation:
            return apology('index', "Password and confirmation do not match")
        elif db.execute("SELECT username FROM users WHERE username = ?", username):
            return apology('index', "Username in use")
        # elif password: will have password conditions here (legth, numbers)
        #     return apology('index', "")
        db.execute("INSERT INTO users(username, hash, date_created) VALUES(?, ?, ?)", username, generate_password_hash(password), datetime.datetime.now())
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
             return apology('login', "Username entry is required")

        if not password:
            return apology('login', "Password entry is required")


        user = db.execute("SELECT id, username, hash FROM users WHERE username = ?", username)

        if not user or not check_password_hash(user[0]["hash"], password):
            return apology('login', "Invalid username/ password")
        session["user_id"] = user[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")
