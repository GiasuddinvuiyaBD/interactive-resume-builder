
from cs50 import SQL 
from flask import Flask, redirect, render_template, session, request
from flask_session import Session

# configure application
app = Flask(__name__)

# configue session to ensure filesystem (insted of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)




# Ensuser that users get up to date data
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def home():
    return render_template("layout.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/register", methods = ["GET","POST"])
def register():

    if request.method == "post" :
        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmPass = request.form.get("confirmation")

        print(name,email,password, confirmPass)

    return render_template("register.html")



