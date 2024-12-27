
import re 
from cs50 import SQL 
from flask import Flask, redirect, render_template, session, request
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology

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

    errors = {}  # Dictionary to store error messages

    if request.method == "POST" :
        name = request.form.get("username").strip()
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()
        confirmPass = request.form.get("confirmation").strip()

        if not name:
          errors["name"] = "User name is required."
        
        # email validation
        if not email:
            errors["email"] = "Please fill out the email field"
        else:
            validEmailPattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(validEmailPattern, email):
                errors["email"] = "Invalid email format"
        
        # password validation
        if not password:
            errors["password"] = "Please fill out the password field"
        elif len(password) < 4:
            errors["password"] = "Password should be min 4 char"
        elif len(password) > 16:
            errors["password"] = "Password should be max 16 char"
        # i will work with making strong password part or generate a strong password

        # confirm password
        if not confirmPass:
            errors["confirmation"] = "Opps! fill out the confirm password"
        elif password != confirmPass:
            errors["confirmation"] = "try again your password is not match"

        
        # hash the password
        if not errors:
            password_hash = generate_password_hash(password)
             # Save user data into the database here
            print(f"Name: {name}, Email: {email}, Password Hash: {password_hash}")
            return redirect("/login") 


    return render_template("register.html", errors=errors)



# Enable debug mode
if __name__ == "__main__":
    app.run(debug=True)