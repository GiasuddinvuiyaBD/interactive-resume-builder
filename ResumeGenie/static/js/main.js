let registrationBtn = document.querySelector("#submitBtn")
// let loginBtn = document.querySelector("#loginBtn")


registrationBtn.addEventListener('click', (evt) => {

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