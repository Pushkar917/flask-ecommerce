function check() {
    if(document.getElementById('password').value !==
            document.getElementById('confirm_password').value) {
            document.getElementById('message').innerHTML = "Password Mismatched";
    }
}