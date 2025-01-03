
let registrationBtn = document.querySelector("#submitBtn")
let loginBtn = document.querySelector("#loginBtn")
let resumeBtn = document.querySelector("#resumeBtn")
let addEductionFieldBtn = document.querySelector("#educationBtn")
let addExperienceBtn = document.querySelector("#experienceBtn")
let addSkillBtn = document.querySelector("#skillsBtn")

let educationSection = document.querySelector(".education-section");
let experience = document.querySelector(".work-experience-section")
let skills = document.querySelector(".skill-section")


if(registrationBtn){
registrationBtn.addEventListener("click", (evt) => {

    // Select input fields
    let userNameField = document.querySelector("#name");
    let emailField = document.querySelector("#email");
    let passwordField = document.querySelector("#password");
    let confirmationField = document.querySelector("#confirmation");
    
    let userName = userNameField.value.trim();
    let email = emailField.value.trim();
    let password = passwordField.value.trim();
    let confirmation = confirmationField.value.trim();
    
    // select error message field
    let nameError = document.querySelector(".name-error")
    let emailError = document.querySelector(".email-error")
    let passwordError = document.querySelector(".password-error")
    let confirmationError = document.querySelector(".confirmation-error")

    // registation field validation
    let error = false;
    let validEmail = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email)

    if(!userName){
        nameError.textContent = "User name is required."
        userNameField.classList.add("is-invalid")
        error = true;
    } else {
        userNameField.classList.remove("is-invalid")
        nameError.textContent = ""
    }

    // email validation
    if(!email){
        emailError.textContent = "Email address is required"
        emailField.classList.add("is-invalid")
        error = true
    } else {
        emailField.classList.remove("is-invalid")
        emailError.textContent = "" 
    }

    if(!validEmail){
        emailError.textContent = "Invalid email format"
        emailField.classList.add("is-invalid")
        error = true
    } else {
        emailField.classList.remove("is-invalid")
        emailError.textContent = "" 
    }

    // password validation
    if(!password){
        passwordError.textContent = "Password is required field"
        passwordField.classList.add("is-invalid")
        error = true;
    } else if(password.length < 4){
        passwordError.innerHTML = `
        Password should be at least 4 characters. <br/>
        <a href="#" id="generate-password" class="text-primary">Generate a strong password</a>
    `;
        passwordField.classList.add("is-invalid")
        error = true;
    } else if(password.length > 16){
        passwordError.innerHTML = `
        Password should be max 16 characters. <br/>
        <a href="#" id="generate-password" class="text-primary">Generate a strong password</a>
    `;
        passwordField.classList.add("is-invalid")
        error = true;
    } else {
        passwordField.classList.remove("is-invalid")
        passwordError.textContent = ""
    }

    if(!confirmation){
        confirmationError.textContent = "Confiramtion is required field"
        confirmationField.classList.add("is-invalid")
        error = true;
    } else {
        confirmationField.classList.remove("is-invalid")
        confirmationError.textContent = ""
    }

    if(password !== confirmation){
        confirmationError.textContent = "Opps! your password is not match"
        error = true
    } else {
        confirmationField.classList.remove("is-invalid")
        confirmationError.textContent = ""
    }

    if(error){
        evt.preventDefault()
    }
})
}


if(loginBtn){
loginBtn.addEventListener('click', (evt) => {
    
    let emailField = document.querySelector("#email")
    let passwordField = document.querySelector("#password")

    let email = emailField.value.trim()
    let password = passwordField.value.trim()

    
    let errors = false;

    if(!email){
        emailField.classList.add("is-invalid")
        errors = true
    } else {
        emailField.classList.remove("is-invalid")
    }

    if(!password){
        passwordField.classList.add("is-invalid")
        errors = true
    }else{
        passwordField.classList.remove("is-invalid")
    }

    if(errors) evt.preventDefault();
})
}    

// resume form validation
// Select fields
const fields = {
    personal: {
        title: document.querySelector("#title"),
        name: document.querySelector("#name"),
        email: document.querySelector("#email"),
        phone: document.querySelector("#phone"),
        address: document.querySelector("#address"),
        linkedin: document.querySelector("#linkedin"),
        portfolio: document.querySelector("#portfolio"),
        professionalSummary: document.querySelector("#professional-summary")
    },
    education: {
        degree: document.querySelector("#degree"),
        institution: document.querySelector("#institution"),
        year: document.querySelector("#year"),
    },
    experience: {
        role: document.querySelector("#role"),
        company: document.querySelector("#company"),
        work_year: document.querySelector("#work_year"),
    },
};

// default value 
fields.personal.title.value = "Software Engineer"
fields.personal.name.value = "Gias uddin vuiya"
fields.personal.email.value = "giasuddin_harvard@gmail.com"
fields.personal.phone.value = "01210001337"
fields.personal.address.value = "Dhaka Bangladesh"
fields.personal.professionalSummary.value = "A concise overview of your career highlights, key skills, and what you bring to the role."
fields.personal.linkedin.value = "https://www.linkedin.com/in/brian-yu/"
fields.personal.portfolio.value = "https://www.protfolio.com"

fields.education.degree.value = "CSE"
fields.education.institution.value = "Harvard"
fields.education.year.value = "2024"

fields.experience.role.value = "Engineer"
fields.experience.company.value = "Microsoft"
fields.experience.work_year.value = "2023"


// Error selectors
const errorSelectors = {
    titleError: document.querySelector(".title-error"),
    nameError: document.querySelector(".name-error"),
    emailError: document.querySelector(".email-error"),
    phoneError: document.querySelector(".phone-error"),
    degreeError: document.querySelector(".degree-error"),
    institutionError: document.querySelector(".institution-error"),
    yearError: document.querySelector(".year-error"),
    finalMessage : document.querySelector(".form-validation-fail")
};

// validate the resume form
if(resumeBtn){
resumeBtn.addEventListener('click', (evt) => {

    // Track validation state
    let errors = false;
    // Validation helpers
    const validateField = (field, errorField, validationFn, errorMsg) => {
        const value = field.value.trim();
        if (!validationFn(value)) {
            errorField.textContent = errorMsg;
            field.classList.add("is-invalid");
            errors = true;
        } else {
            errorField.textContent = "";
            field.classList.remove("is-invalid");
        }
    };

    // 
    const isRequired = (value) => value.length > 0;
    const isEmail = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
    const isPhone = (value) => /^\+?\d{10,15}$/.test(value); // Supports international format
    const isYear = (value) => /^\d{4}$/.test(value) && value >= 1900 && value <= new Date().getFullYear();

    // Personal Info Validation
    validateField(fields.personal.title, errorSelectors.titleError, isRequired, "Title is required.");
    validateField(fields.personal.name, errorSelectors.nameError, isRequired, "Name is required.");
    validateField(fields.personal.email, errorSelectors.emailError, isEmail, "Enter a valid email address.");
    validateField(fields.personal.phone, errorSelectors.phoneError, isPhone, "Enter a valid phone number (10-15 digits).");

    // Education Validation
    validateField(fields.education.degree, errorSelectors.degreeError, isRequired, "Degree is required.");
    validateField(fields.education.institution, errorSelectors.institutionError, isRequired, "Institution is required.");
    validateField(fields.education.year, errorSelectors.yearError, isYear, "Enter a valid year (e.g., 2024).");

    // 
    if(errors){
        errorSelectors.finalMessage.textContent = "From validation fail! Please correct the error and try again"
        evt.preventDefault()
        return
    }else{
        errorSelectors.finalMessage.textContent = "Form submitted successfully!";
        //  i will work with reset functionality later 
        // reset()
    }  
})
}


const reset = (() => {
    // Clear static fields
    fields.personal.title.value = "";
    fields.personal.name.value = "";
    fields.personal.email.value = "";
    fields.personal.phone.value = "";
    fields.personal.professionalSummary.value = ""
    // fields.personal.country && (fields.personal.country.value = ""); // Optional field
    // fields.personal.city && (fields.personal.city.value = "");       // Optional field
    fields.personal.portfolio && (fields.personal.address.value = "");
    fields.personal.linkedin && (fields.personal.linkedin.value = "");
    fields.personal.portfolio && (fields.personal.portfolio.value = "");
    

    fields.education.degree.value = "";
    fields.education.institution.value = "";
    fields.education.year.value = "";

    fields.experience.role.value = "";
    fields.experience.company.value = "";
    fields.experience.work_year && (fields.experience.work_year.value = ""); // Optional field

    // Remove dynamically added fields
    const dynamicEducationItems = document.querySelectorAll(".education-item.row");
    dynamicEducationItems.forEach(item => item.remove());

    const dynamicExperienceItems = document.querySelectorAll(".experience-item.row");
    dynamicExperienceItems.forEach(item => item.remove());

    // Optionally, reset the form completely
    const form = document.querySelector("#yourFormID"); // Replace with your form's ID
    form.reset();

    evt.preventDefault(); // Prevent default form submission
})

// add education field
if(addEductionFieldBtn){
addEductionFieldBtn.addEventListener('click', (evt) => {

    evt.preventDefault()
    const newEducation = `
        <div class="education-item row mb-3">
            <div class="col">
                <div class="form-group mb-4">
                    <input class="form-control" id="degree" name="degree" placeholder="Degree: " type="text">
                    <small class="form-text text-muted"></small>
                </div>
            </div>
            <div class="col">
                <div class="form-group mb-4">
                    <input class="form-control" id="institution" name="institution" placeholder="Institution: " type="text">
                    <small class="form-text text-muted"></small>
                </div>
            </div>
            <div class="col">
                <div class="form-group mb-4">
                    <input class="form-control" id="year" name="year" placeholder="Year: " type="text">
                    <small class="form-text text-muted"></small>
                </div>
            </div>
            <button type="button" class="btn btn-sm btn-outline-danger mb-4 remove-btn">Remove</button> 
        </div>`;
    educationSection.insertAdjacentHTML("beforeend", newEducation);
})
}


if(addExperienceBtn){
addExperienceBtn.addEventListener('click', (evt) => {
    evt.preventDefault();
    
    let newExperience = `
            <div class="education-item form-row mb-3">
                <div class="col">
                    <div class="form-group mb-5">
                        <input class="form-control" id="role" name="role" placeholder="Role: " type="text">
                        <small class="form-text text-muted"></small>
                    </div>
                </div>
                <div class="col">
                    <div class="form-group mb-5">
                        <input class="form-control" id="company" name="company" placeholder="Company: " type="text">
                        <small class="form-text text-muted"></small>
                    </div>
                </div>
                <div class="col">
                    <div class="form-group mb-5">
                        <input class="form-control" id="work_year" name="work_year" placeholder="Year: " type="text">
                        <small class="form-text text-muted"></small>
                    </div>
                </div>
                <button type="button" class="btn btn-sm btn-outline-danger mb-4 remove-btn">Remove</button> 
            </div>
    `
    experience.insertAdjacentHTML("beforeend", newExperience)

})
}


if(addSkillBtn) {
addSkillBtn.addEventListener('click', (evt) => {
    let newSkills = `
        <div class="skill-item form-row mb-3">
            <div class="col">
                <div class="form-group mb-5">
                    <input class="form-control" id="skill" name="skill" placeholder="Write you skills " type="text">
                    <small class="form-text text-muted"></small>
                </div>
            </div>
            <button type="button" class="btn btn-sm btn-outline-danger mb-4 remove-btn">Remove</button> 
        </div>
    `
    skills.insertAdjacentHTML('beforeend', newSkills)
})
}
 
// Event delegation for the remove functionality
if(educationSection){
educationSection.addEventListener("click", (evt) => {
    if (evt.target.classList.contains("remove-btn")) {
        evt.target.parentElement.remove(); 
    }
});
}


if(experience){
experience.addEventListener("click", (evt) =>{
    if (evt.target.classList.contains("remove-btn")) {
        evt.target.parentElement.remove(); 
    }
})
}

if(skills){
skills.addEventListener("click", (evt) =>{
    if (evt.target.classList.contains("remove-btn")) {
        evt.target.parentElement.remove(); 
    }
})
}

