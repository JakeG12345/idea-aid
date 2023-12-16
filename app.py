# import os

# from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
# from flask_session import Session
# from werkzeug.security import check_password_hash, generate_password_hash
#TEST IF ASHER CAN COMMIT
#JACOB
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")