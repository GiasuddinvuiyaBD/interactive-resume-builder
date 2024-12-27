let registrationBtn = document.querySelector("#submitBtn")


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
        userName.style.border = "1px solid green"
        error = true;
    } else {
        nameError.textContent = ""
    }

    // email validation
    if(!email){
        emailError.textContent = "Email address is required"
        error = true
    } else if(!validEmail){
        emailError.textContent = "Invalid email format"
        error = true
    } else {
        email.textContent = "" 
    }

    // password validation
    if(!password){
        passwordError.textContent = "Password is required field"
        error = true;
    } else if(password.length < 4){
        passwordError.innerHTML = `
        Password should be at least 4 characters. <br/>
        <a href="#" id="generate-password" class="text-primary">Generate a strong password</a>
    `;
        error = true;
    } else if(password.length > 16){
        passwordError.innerHTML = `
        Password should be max 16 characters. <br/>
        <a href="#" id="generate-password" class="text-primary">Generate a strong password</a>
    `;
        error = true;
    } else {
        passwordError.textContent = ""
    }

    if(!confirmation){
        confirmationError.textContent = "Confiramtion is required field"
        error = true;
    } else {
        confirmationError.textContent = ""
    }

    if(password !== confirmation){
        confirmationError.textContent = "Opps! your password is not match"
        error = true
    } else {
        confirmationError.textContent = ""
    }

    if(error){
        evt.preventDefault()
    }
})