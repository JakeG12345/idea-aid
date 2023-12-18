import os

# from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
# from flask_session import Session
# from werkzeug.security import check_password_hash, generate_password_hash
import openai

app = Flask(__name__)

@app.route("/")
def index():
    
    print("YO 2")
    
    print("api key:", os.environ.get("OPENAI_API_KEY"))
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input="The food was delicious and the waiter..."
    )

    print(response)

    return render_template("index.html")