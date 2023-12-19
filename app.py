import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
# from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology, datetime
from openai import OpenAI
client = OpenAI()

app = Flask(__name__)

# consists of tuples with format (question, answer)
# quiz_selections = []

db = SQL("sqlite:///db.db")

@app.route("/")
@login_required
def index():
    # print(completion.choices[0].message)

    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    quiz_selections = []

    if request.method == "POST":
        selection = request.form.get("option")
        print(selection)
        # global quiz_selections
        # quiz_selections.append(selection)

    pastSelections = ""
    for selection in quiz_selections:
        pastSelections = pastSelections + f" - Question: {selection[0]}, answer: {selection[1]}"
    if pastSelections != "":
        pastSelections = "Here are past question and answers: " + pastSelections

    content = ""

    while content.count('::') != 1:
        data = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Query is coming from an app that helps users come up with ideas through the help of AI. It does this through a series of multiple choice questions that lead to a idea. For question {len(quiz_selections) + 1}, give me a question and a few answers. Remember, question should follow past questions to help lead into an idea for the user. Depending on how far along the question, the more or less specific it should be.{pastSelections}. IMPORTANT: You should return the question, followed by a '::' (without a space inbetween), followed by the possible answers comma separated without a space inbetween. In other words it should look like 'This is the question?::option 1, another option i guess' and you probably will have more options."
                }
            ]
        )
        content = data.choices[0].message.content

    print("Message:", content)
    
    question, optionsD = data.choices[0].message.content.split("::")
    options = optionsD.split(",")
    print("Quiz selections:", quiz_selections)
    print("Options:", options)

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