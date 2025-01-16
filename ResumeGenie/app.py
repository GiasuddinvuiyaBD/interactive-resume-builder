import re 
import json
import pdfkit
from cs50 import SQL 
from flask import Flask, flash, redirect, render_template, session, request, jsonify, url_for, send_file
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology , login_required
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

@app.route("/dashbord")
def dashbord():
    return render_template("dashbord.html")

@app.route("/resume", methods=["GET"])
@login_required
def resume():
    try:
        user_id = session["user_id"]
        # Fetch all resumes from the database
        resumes = db.execute("SELECT * FROM resumes WHERE user_id = ?", user_id)
        
        # Process JSON fields for proper rendering in the UI
        for resume in resumes:
            if 'education' in resume and resume['education']:
                resume['education'] = json.loads(resume['education'])
            if 'work_experience' in resume and resume['work_experience']:
                resume['work_experience'] = json.loads(resume['work_experience'])
            if 'skills' in resume and resume['skills']:
                resume['skills'] = json.loads(resume['skills'])

        # Pass resumes to the template
        return render_template("resume.html", resumes=resumes)
    except Exception as e:
        app.logger.error(f"Error fetching resumes: {e}")
        flash("An error occurred while fetching resumes.")
        return render_template("resume.html", resumes=[])


# @app.route("/resume/<int:resume_id>")
@app.route("/resume/<int:resume_id>", methods=["DELETE"])
@login_required
def remove_resume(resume_id):
    """Remove specific resume via AJAX."""
    try:
        user_id = session["user_id"]
        resume = db.execute("SELECT * FROM resumes WHERE id = ? AND user_id = ?", resume_id, user_id)

        if not resume:
            return jsonify({"error": "Resume not found or permission denied."}), 403

        db.execute("DELETE FROM resumes WHERE id = ? AND user_id = ?", resume_id, user_id)
        return jsonify({"message": "Resume deleted successfully."}), 200

    except Exception as e:
        app.logger.error(f"Error deleting resume {resume_id}: {e}")
        return jsonify({"error": "An error occurred while deleting the resume."}), 500


@app.route("/resume/pdf/<int:resume_id>")
@login_required
def download_pdf(resume_id):
    """Generate a PDF for a specific resume"""
    try:
        user_id = session["user_id"]
        # Fetch the specific resume
        resume = db.execute("SELECT * FROM resumes WHERE id = ? AND user_id = ?", resume_id, user_id)
        if not resume:
            flash("Resume not found.")
            return redirect("/resume")

        resume = resume[0]
        resume['education'] = json.loads(resume['education']) if resume['education'] else []
        resume['work_experience'] = json.loads(resume['work_experience']) if resume['work_experience'] else []
        resume['skills'] = json.loads(resume['skills']) if resume['skills'] else []

        # Render the resume to an HTML template
        rendered_html = render_template("resume_pdf_template.html", resume=resume)

        # Configure PDFKit
        pdfkit_options = {
            "enable-local-file-access": True
        }
        pdf = pdfkit.from_string(rendered_html, False, options=pdfkit_options)

        # Return PDF as a downloadable file
        response = app.response_class(
            pdf,
            mimetype="application/pdf",
            headers={
                "Content-Disposition": f"attachment;filename={resume['title']}.pdf"
            }
        )
        return response
    except Exception as e:
        app.logger.error(f"Error generating PDF: {e}")
        flash("An error occurred while generating the PDF.")
        return redirect("/resume")


@app.route("/resume/edit/<int:resume_id>", methods=["GET", "POST"])
@login_required
def edit_resume(resume_id):

    try:
        # Get the logged-in user's ID
        user_id = session["user_id"]

        # Fetch the resume from the database
        resume = db.execute("SELECT * FROM resumes WHERE id = ? AND user_id = ?", resume_id, user_id)

        # Check if the resume exists and belongs to the user
        if not resume:
            flash("Resume not found or you don't have permission to edit it.", "warning")
            return redirect("/resume")
        
        # Decode JSON fields (assuming education, work_experience, skills are stored as JSON)
        resume = resume[0]
        resume["education"] = json.loads(resume["education"]) if resume.get("education") else []
        resume["work_experience"] = json.loads(resume["work_experience"]) if resume.get("work_experience") else []
        resume["skills"] = json.loads(resume["skills"]) if resume.get("skills") else []


        # If the request method is POST, process the form submission
        if request.method == "POST":
            # Extract form data
            title = request.form.get("title")
            name = request.form.get("name")
            email = request.form.get("email")
            phone = request.form.get("phone")
            address = request.form.get("address")
            linkedin = request.form.get("linkedin")
            portfolio = request.form.get("portfolio")
            professional_summary = request.form.get("professional-summary")



            # Extract education, work experience, and skills
            degrees = request.form.getlist("degree")
            institutions = request.form.getlist("institution")
            years = request.form.getlist("year")

            user_id = session["user_id"]

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

            # Validate form inputs (Optional)
            if not title or not name or not email:
                flash("Title, Name, and Email are required fields.", "danger")
                return render_template("edit_resume.html", resume=resume[0])

            # Update the resume in the database
            db.execute(
                """
                UPDATE resumes 
                SET title = ?, name = ?, email = ?, phone = ?, address = ?, linkedin = ?, portfolio = ?, professional_summary = ? , education = ?, work_experience = ?, skills = ?
                WHERE id = ? AND user_id = ?
                """,
                title, name, email, phone, address, linkedin, portfolio, professional_summary, json.dumps(education), json.dumps(work_experience), json.dumps(skills), resume_id, user_id
            )

            flash("Resume updated successfully!", "success")
            return redirect("/resume")

        # If GET request, render the form with the existing resume details
        return render_template("edit_resume.html", resume=resume)

    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        return redirect("/resume")

    

@app.route("/form", methods=["GET", "POST"])
@login_required
def form():

    errors = {}

    if request.method == "POST":
        # Get form data
        title = request.form.get("title", "").strip()
        name = request.form.get("name", "").strip()
        email = request.form.get("email_", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        linkedin = request.form.get("linkedin", "").strip()
        portfolio = request.form.get("portfolio", "").strip()
        professional_summary = request.form.get("professional-summary", "").strip()

        # Extract education, work experience, and skills
        degrees = request.form.getlist("degree")
        institutions = request.form.getlist("institution")
        years = request.form.getlist("year")

        user_id = session["user_id"]

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
            db.execute("INSERT INTO resumes (user_id, title, name, email, phone,  address, linkedin, portfolio,professional_summary, education, work_experience, skills) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user_id, title, name, email, phone, address, linkedin, portfolio or "", professional_summary, json.dumps(education), json.dumps(work_experience), json.dumps(skills))
            
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
        # print(user)

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


@app.route("/templates", methods=["GET"])
def templates():

    try:
        # Fetch all resumes from the database
        resumes = db.execute("SELECT * FROM resumes")
        
        for resume in resumes:
            if 'education' in resume and resume['education']:
                resume['education'] = json.loads(resume['education'])
            if 'work_experience' in resume and resume['work_experience']:
                resume['work_experience'] = json.loads(resume['work_experience'])
            if 'skills' in resume and resume['skills']:
                resume['skills'] = json.loads(resume['skills'])

         # Add template choices dynamically
        template_s = ['template-1.html', 'template-2.html', 'template-3.html']
        for i, resume in enumerate(resumes):
            resume['template'] = template_s[i % len(template_s)]  # Rotate through templates


        return render_template('templates.html', resumes=resumes)
    except Exception as e:
        app.logger.error(f"Error fetching resumes: {e}") 
        flash("An error occurred while fetching resumes.")
        return render_template("templates.html", resumes=[])

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
