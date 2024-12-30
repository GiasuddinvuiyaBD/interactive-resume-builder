
let registrationBtn = document.querySelector("#submitBtn")
let loginBtn = document.querySelector("#loginBtn")
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

// add education field
addEductionFieldBtn.addEventListener('click', (evt) => {
    
    evt.preventDefault()
    const newEducation = `
        <div class="education-item row mb-3">
            <div class="col">
                <div class="form-group mb-4">
                    <input class="form-control" id="degree" name="[]" placeholder="Degree: " type="text">
                    <small class="form-text text-muted"></small>
                </div>
            </div>
            <div class="col">
                <div class="form-group mb-4">
                    <input class="form-control" id="institution" name="[]" placeholder="Institution: " type="text">
                    <small class="form-text text-muted"></small>
                </div>
            </div>
            <div class="col">
                <div class="form-group mb-4">
                    <input class="form-control" id="year" name="[]" placeholder="Year: " type="text">
                    <small class="form-text text-muted"></small>
                </div>
            </div>
            <button type="button" class="btn btn-sm btn-outline-danger mb-4 remove-btn">Remove</button> 
        </div>`;
    educationSection.insertAdjacentHTML("beforeend", newEducation);
})

addExperienceBtn.addEventListener('click', (evt) => {
    evt.preventDefault();
    
    let newExperience = `
            <div class="education-item form-row mb-3">
                <div class="col">
                    <div class="form-group mb-5">
                        <input class="form-control" id="role" name="[]" placeholder="Role: " type="text">
                        <small class="form-text text-muted"></small>
                    </div>
                </div>
                <div class="col">
                    <div class="form-group mb-5">
                        <input class="form-control" id="company" name="[]" placeholder="Company: " type="text">
                        <small class="form-text text-muted"></small>
                    </div>
                </div>
                <div class="col">
                    <div class="form-group mb-5">
                        <input class="form-control" id="year" name="[]" placeholder="Year: " type="text">
                        <small class="form-text text-muted"></small>
                    </div>
                </div>
                <button type="button" class="btn btn-sm btn-outline-danger mb-4 remove-btn">Remove</button> 
            </div>
    `
    experience.insertAdjacentHTML("beforeend", newExperience)

})

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
 
// Event delegation for the remove functionality
educationSection.addEventListener("click", (evt) => {
    if (evt.target.classList.contains("remove-btn")) {
        evt.target.parentElement.remove(); 
    }
});

experience.addEventListener("click", (evt) =>{
    if (evt.target.classList.contains("remove-btn")) {
        evt.target.parentElement.remove(); 
    }
})

skills.addEventListener("click", (evt) =>{
    if (evt.target.classList.contains("remove-btn")) {
        evt.target.parentElement.remove(); 
    }
})

