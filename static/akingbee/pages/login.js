function validateLogin(){
    let data = {
        username: $("#username").val(),
        password: $("#password").val()
    };
    
    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/login";
    
    $.ajax({
        type: "POST",
        url: my_url,
        data: data,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            showSuccess(answer);
            location = root_path + "/";
        }
    });

    return false;
}


function forgot_password(){
    let myUrl = window.location.protocol + "//" + window.location.host + "/akingbee/reset_password";
    window.location = myUrl;
}

