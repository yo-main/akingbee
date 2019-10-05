function validateLogin(){
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

    return false;
}


function forgot_password(){
    let myUrl = get_full_url("/reset_password");
    window.location = myUrl;
}

