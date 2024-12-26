
from cs50 import SQL 
from flask import Flask, redirect, render_template, session, request
from flask_session import Session

# configure application
app = Flask(__name__)

# configue session to ensure filesystem (insted of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def home():

    return render_template("layout.html")


