$("#login-form").submit( function(event) {
    event.preventDefault();

    let data = {
        username: $("#username").val(),
        password: $("#password").val()
    };

    let my_url = get_full_url("/login");

    $.ajax({
        type: "POST",
        url: my_url,
        data: data,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            showSuccess(answer);
            window.location.href = get_full_url("/");
        }
    });
});


function forgot_password() {
    let myUrl = get_full_url("/reset_password");
    window.location = myUrl;
}


$("#reset-form").submit( function(event) {
    event.preventDefault();

    let username = $("#username").val();
    let pwd1 = $("#password").val();
    let pwd2 = $("#passwordConfirmation").val();

    if (username == '' || pwd1 == '' || pwd2 == ''){
        return false;
    }

    if (pwd1 != pwd2){
        if (LANGUAGE == "fr"){
            createError("Les mots de passes ne sont pas identique");
        }
        else{
            createError("The passwords are not matching");
        }

        return false;
    }

    url = get_full_url("/reset_password");
    data = {username: username, pwd: pwd1}

    $.ajax({
        type: "POST",
        url: url,
        data: data,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            showSuccess(answer);
            window.location.href = get_full_url("/");
        }
    });
});
