function validate_registration(){
    let language = $("html").attr("lang");
    let username = $("#username").val();
    let email = $("#email").val();
    let pwd = $("#password").val();
    let verify_pwd = $("#verify_password").val();

    if (username == '' || email == '' || pwd == '' || verify_pwd == ''){
        if (language == "fr"){
            createError("Merci de remplir tous les champs");
        }
        else{
            createError("Please fill-in every fields");
        }

        return false;
    }
    
    if (pwd != verify_pwd){
        if (language == "fr"){
            createError("Les mots de passes ne sont pas identiques");
        }
        else{
            createError("The passwords are not matching");
        }
        
        return false;
    }

    $.ajax({
        url: "registercheck",
        type: "POST",
        data: {username: username,
               email: email,
               pwd: pwd},
        dataType: 'json',
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
