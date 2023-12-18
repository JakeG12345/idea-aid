import os

# from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
# from flask_session import Session
# from werkzeug.security import check_password_hash, generate_password_hash
from openai import OpenAI
client = OpenAI()

app = Flask(__name__)

# consists of tuples with format (question, answer)
# quiz_selections = []

@app.route("/")
def index():
    # print(completion.choices[0].message)

    return render_template("index.html")

@app.route("/quiz")
def quiz():
    quiz_selections = []

    if request.method == "POST":
        selection = request.form.get("option")
        # global quiz_selections
        # quiz_selections.append(selection)

    pastSelections = ""
    for selection in quiz_selections:
        pastSelections = pastSelections + f" - Question: {selection[0]}, answer: {selection[1]}"
    if pastSelections != "":
        pastSelections = "Here are past question and answers: " + pastSelections

    content = ""

    while '::' not in content:
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

    # return render_template("index.html")

    return render_template("quiz.html", question=question, options=options)