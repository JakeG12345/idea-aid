import os

# from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
# from flask_session import Session
# from werkzeug.security import check_password_hash, generate_password_hash
from openai import OpenAI
client = OpenAI()

app = Flask(__name__)

@app.route("/")
def index():
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ]
    )

    print(completion.choices[0].message)

    return render_template("index.html")