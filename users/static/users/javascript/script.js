//const emailError = document.querySelector("#email + span.error");
//const usernameError = document.querySelector("#username + span.error");
//
//const signupForm = document.querySelector("#signup");
//const loginForm = document.querySelector("#login");
//
//const pwd1Error = document.querySelector("#pwd1 + span.error");
//const pwd2Error = document.querySelector("#pwd2 + span.error");
//
//const signupLink = document.querySelector("#signuplink");
//const loginLink = document.querySelector("#loginlink");
//
//const allErrors = document.querySelectorAll("span.error");
//
//allErrors.forEach((error) => {
//  error.classList.add("xhide");
//});
//
//function checkForm(form) {
//  let formValid = true;
//  if (form.username.value == "") {
//    usernameError.textContent = "Username cannot be blank!";
//    form.username.focus();
//    if (usernameError.classList.contains("xhide"))
//      usernameError.classList.remove("xhide");
//    formValid = false;
//  } else {
//    re = /^\w+$/;
//    if (!re.test(form.username.value)) {
//      usernameError.textContent =
//        "Username must contain only letters, numbers and underscores!";
//      form.username.focus();
//      if (usernameError.classList.contains("xhide"))
//        usernameError.classList.remove("xhide");
//      formValid = false;
//    }
//  }
//
//  if (form.pwd1.value != "" && form.pwd1.value == form.pwd2.value) {
//    if (form.pwd1.value.length < 6) {
//      pwd1Error.textContent = "Password must contain at least six characters!";
//      form.pwd1.focus();
//      if (pwd1Error.classList.contains("xhide"))
//        pwd1Error.classList.remove("xhide");
//      formValid = false;
//    }
//    if (form.pwd1.value == form.username.value) {
//      pwd1Error.textContent = "Password must be different from Username!";
//      form.pwd1.focus();
//      if (pwd1Error.classList.contains("xhide"))
//        pwd1Error.classList.remove("xhide");
//      formValid = false;
//    }
//    re = /[0-9]/;
//    if (!re.test(form.pwd1.value)) {
//      pwd1Error.textContent =
//        "password must contain at least one number (0-9)!";
//      form.pwd1.focus();
//      if (pwd1Error.classList.contains("xhide"))
//        pwd1Error.classList.remove("xhide");
//      formValid = false;
//    }
//    re = /[a-z]/;
//    if (!re.test(form.pwd1.value)) {
//      pwd1Error.textContent =
//        "password must contain at least one lowercase letter (a-z)!";
//      form.pwd1.focus();
//      if (pwd1Error.classList.contains("xhide"))
//        pwd1Error.classList.remove("xhide");
//      formValid = false;
//    }
//    re = /[A-Z]/;
//    if (!re.test(form.pwd1.value)) {
//      pwd1Error.textContent =
//        "password must contain at least one uppercase letter (A-Z)!";
//      form.pwd1.focus();
//      if (pwd1Error.classList.contains("xhide"))
//        pwd1Error.classList.remove("xhide");
//      formValid = false;
//    }
//  } else {
//    pwd1Error.textContent =
//      "Please check that you've entered and confirmed your password!";
//    form.pwd1.focus();
//    if (pwd1Error.classList.contains("xhide"))
//      pwd1Error.classList.remove("xhide");
//    formValid = false;
//  }
//
//  if (form.email.value == "") {
//    emailError.textContent = "Email cannot be blank!";
//    form.email.focus();
//    if (emailError.classList.contains("xhide"))
//      emailError.classList.remove("xhide");
//    formValid = false;
//  } else {
//    re = /^\S+@\S+[\.][0-9a-z]+$/;
//    if (!re.test(form.email.value)) {
//      emailError.textContent = "Email is invalid!";
//      form.email.focus();
//      if (emailError.classList.contains("xhide"))
//        emailError.classList.remove("xhide");
//      formValid = false;
//    }
//  }
//
//  return formValid;
//}
//
//function checkLoginForm(form) {
//  let formValid = true;
//  if (form.username.value == "") {
//    usernameError.textContent = "Username cannot be blank!";
//    form.username.focus();
//    if (usernameError.classList.contains("xhide"))
//      usernameError.classList.remove("hide");
//    formValid = false;
//  }
//  re = /^\w+$/;
//  if (!re.test(form.username.value)) {
//    usernameError.textContent =
//      "Username must contain only letters, numbers and underscores!";
//    form.username.focus();
//    if (usernameError.classList.contains("hide"))
//      usernameError.classList.remove("hide");
//    formValid = false;
//  }
//
//  if (form.pwd1.value != "") {
//    if (form.pwd1.value.length < 6) {
//      pwd1Error.textContent = "Password must contain at least six characters!";
//      form.pwd1.focus();
//      if (pwd1Error.classList.contains("hide"))
//        pwd1Error.classList.remove("hide");
//      formValid = false;
//    }
//    if (form.pwd1.value == form.username.value) {
//      pwd1Error.textContent = "Password must be different from Username!";
//      form.pwd1.focus();
//      if (pwd1Error.classList.contains("hide"))
//        pwd1Error.classList.remove("hide");
//      formValid = false;
//    }
//    re = /[0-9]/;
//    if (!re.test(form.pwd1.value)) {
//      pwd1Error.textContent =
//        "password must contain at least one number (0-9)!";
//      form.pwd1.focus();
//      if (pwd1Error.classList.contains("hide"))
//        pwd1Error.classList.remove("hide");
//      formValid = false;
//    }
//    re = /[a-z]/;
//    if (!re.test(form.pwd1.value)) {
//      pwd1Error.textContent =
//        "password must contain at least one lowercase letter (a-z)!";
//      form.pwd1.focus();
//      if (pwd1Error.classList.contains("hide"))
//        pwd1Error.classList.remove("hide");
//      formValid = false;
//    }
//    re = /[A-Z]/;
//    if (!re.test(form.pwd1.value)) {
//      pwd1Error.textContent =
//        "password must contain at least one uppercase letter (A-Z)!";
//      form.pwd1.focus();
//      if (pwd1Error.classList.contains("hide"))
//        pwd1Error.classList.remove("hide");
//      formValid = false;
//    }
//  } else {
//    pwd1Error.textContent = "Please check that you've entered your password!";
//    form.pwd1.focus();
//    if (pwd1Error.classList.contains("hide"))
//      pwd1Error.classList.remove("hide");
//    formValid = false;
//  }
//
//  return formValid;
//}
//
//document.querySelectorAll("input").forEach((inp) =>
//  inp.addEventListener("focusout", function (event) {
//    event.preventDefault();
//    clearError(this);
//  })
//);
//
//function clearError(inp) {
//  let key = [inp.id + "Error"];
//  const { [key]: name } = { usernameError, emailError, pwd1Error, pwd2Error };
//
//  if (inp.id && document.querySelector(`#${inp.id}`).value) {
//    name.textContent = "";
//    if (name.classList.contains("hide")) name.classList.add("hide");
//  }
//}
//
//signupLink.addEventListener("click", (e) => {
//  e.preventDefault();
//  loginForm.classList.toggle("hide");
//  signupForm.classList.toggle("hide");
//});
//
//loginLink.addEventListener("click", (e) => {
//  e.preventDefault();
//  loginForm.classList.toggle("hide");
//  signupForm.classList.toggle("hide");
//});