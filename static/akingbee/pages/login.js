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

$("#reset-form-request").submit( function(event) {
    event.preventDefault();

    let data = {"username": $("#username").val()}

    $.ajax({
        type: "POST",
        data: data,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            showSuccess(answer);
            window.location.href = get_full_url("/");
        }
    });
})

$("#reset-form").submit( function(event) {
    event.preventDefault();

    let pwd1 = $("#password").val();
    let pwd2 = $("#passwordConfirmation").val();

    if (pwd1 != pwd2){
        if (LANGUAGE == "fr"){
            createError("Les mots de passes ne sont pas identiques");
        }
        else{
            createError("The passwords are not matching");
        }

        return false;
    }

    data = {password: pwd1}

    $.ajax({
        type: "POST",
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
