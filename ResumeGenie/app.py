
import re 
import json
from cs50 import SQL 
from flask import Flask, flash, redirect, render_template, session, request, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology
from sqlite3 import IntegrityError
# configure application
app = Flask(__name__)

# configue session to ensure filesystem (insted of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# configure cs50 library to join the sqlite database
db = SQL("sqlite:///users_and_resumes.db")


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
    return render_template("home.html")

@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route("/form", methods=["GET", "POST"])
def form():
    errors = {}

    if request.method == "POST":
        # Get form data
        title = request.form.get("title", "").strip()
        name = request.form.get("name", "").strip()
        email = request.form.get("email_", "").strip()
        phone = request.form.get("phone", "").strip()
        country = request.form.get("country", "").strip()
        city = request.form.get("city", "").strip()
        linkedin = request.form.get("linkedin", "").strip()
        portfolio = request.form.get("portfolio", "").strip()

        # Extract education, work experience, and skills
        degrees = request.form.getlist("degree")
        institutions = request.form.getlist("institution")
        years = request.form.getlist("year")

        #  
        education = [
            {"degree": degree.strip(), "institution": institution.strip(), "year": year.strip()}
            for degree, institution, year in zip(degrees, institutions, years)
        ]

        work_experience = [
            {"role": role.strip(), "company": company.strip(), "year": work_year.strip()}
            for role, company, work_year in zip(
                request.form.getlist("role"),
                request.form.getlist("company"),
                request.form.getlist("work_year")
            )
        ]

        skills = [skill.strip() for skill in request.form.getlist("skill")]

        # Title validation
        if not title:
            errors["title"] = "Title is required."

        # Name validation
        if not name:
            errors["name"] = "Name is required."

        # Email validation
        if not email:
            errors["email"] = "Email is required."
        elif not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            errors["email"] = "Invalid email format."

        # Phone validation
        if not phone:
            errors["phone"] = "Phone number is required."
        elif not re.match(r"^\+?\d{10,15}$", phone):
            errors["phone"] = "Phone number must be 10-15 digits long."

        # Education validation
        for index, edu in enumerate(education):
            if not edu["degree"]:
                errors[f"degree_{index}"] = f"Degree for entry {index + 1} is required."
            if not edu["institution"]:
                errors[f"institution_{index}"] = f"Institution for entry {index + 1} is required."
            if not edu["year"] or not edu["year"].isdigit() or len(edu["year"]) != 4:
                errors[f"year_{index}"] = f"Year for entry {index + 1} must be a 4-digit number."

        # If errors exist, return them to the form
        if errors:
            return render_template("form.html", errors=errors, form_data=request.form)

        # Insert into the database
        try:
            # Why it's not working i don't know -----
            # db.execute('''
            #     INSERT INTO resumes_r (
            #         title, name, email, phone, country, city, linkedin, portfolio, education, work_experience, skills
            #     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            # ''', (
            #     title, name, email, phone, country, city, linkedin, portfolio or "",
            #     json.dumps(education), json.dumps(work_experience), json.dumps(skills)
            # ))

            db.execute("INSERT INTO resumes_r (title, name, email, phone, country, city, linkedin, portfolio, education, work_experience, skills) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", title, name, email, phone, country, city, linkedin, portfolio or "", json.dumps(education), json.dumps(work_experience), json.dumps(skills))

            
            flash("Resume submitted successfully!")
            return redirect("/resume")
        except Exception as e:
            # Log the error for debugging
            app.logger.error(f"Database error: {e}")
            flash("An error occurred while saving your resume. Please try again.")
            return render_template("form.html", errors=errors, form_data=request.form)


    return render_template("form.html", errors=errors, form_data={})
  

@app.route("/login", methods = ["GET", "POST"])
def login():
    
    if request.method == "POST":
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()

        user = db.execute("SELECT * FROM users WHERE email = ?", email)
        print(user)

        if len(user) != 1: 
            flash("Invalid email or password")
            return redirect("/login")
        
        if not check_password_hash(user[0]["password_hash"], password):
            flash("Invalid email or password")
            return redirect("/login")

        # if password match then log the user in
        session["user_id"] = user[0]["id"]
        flash("login successful")
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods = ["GET","POST"])
def register():

    errors = {}  # Dictionary to store error messages. 

    if request.method == "POST" :
        name = request.form.get("username").strip()
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()
        confirmPass = request.form.get("confirmation").strip()


        # Validate name
        if not name:
            errors["name"] = "User name is required."

        # Validate email
        elif not email:
            errors["email"] = "Please fill out the email field"
        else:
            validEmailPattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(validEmailPattern, email):
                errors["email"] = "Invalid email format"

        # Validate password
        if not errors and not password:
            errors["password"] = "Please fill out the password field"
        elif not errors and len(password) < 4:
            errors["password"] = "Password should be min 4 characters"
        elif not errors and len(password) > 16:
            errors["password"] = "Password should be max 16 characters"

        # Validate confirm password
        elif not errors and not confirmPass:
            errors["confirmation"] = "Opps! fill out the confirm password"
        elif not errors and password != confirmPass:
            errors["confirmation"] = "Try again; your passwords do not match"


        # hash the password
        if not errors:
            password_hash = generate_password_hash(password)
            # Save users data into the database here
            try:
                db.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", name, email, password_hash)         
                # Redirect to login page
                flash("Registered successfully! Please log in.")
                return redirect("/login")
            except ValueError:
                errors["email"] = "Email already exists!"
                return render_template("register.html", errors=errors)
            
    return render_template("register.html", errors=errors)



# Enable debug mode
if __name__ == "__main__":
    app.run(debug=True)