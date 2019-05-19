
function new_health(){
    let data = {
        name_fr: $("#health_name_fr").val(),
        name_en: $('#health_name_en').val()
    };

    let language = $('html').attr("lang");
    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/beehouse/create/new_health";

    if ((data.name_fr == "") && (data.name_en == "")){
        if (language == "fr"){
            createError("Merci de compléter au moins un des deux champs");
        }
        else{
            createError("Please fill-in at least one of the two fields");
        }
        return false;
    }

    $.ajax({
        type: "POST",
        url: my_url,
        data: data,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            $("#create_health").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });

    return false;
}


function new_owner(){
    let data = {owner: $("#owner_name").val()};
    let language = $("html").attr("lang");

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/beehouse/create/new_owner";

    if (data.owner == ""){
        if (language == "fr"){
            createError("Merci de compléter tous les champs");
        }
        else{
            createError("Please fill-in every fields");
        }
        return false;
    }

    $.ajax({
        type: "POST",
        url: my_url,
        data: data,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            $("#create_owner").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });

    return false;
}




function new_status_beehouse(){
    let data = {
        name_fr: $("#status_beehouse_name_fr").val(),
        name_en: $('#status_beehouse_name_en').val()
    };

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/beehouse/create/new_beehouse_status";

    if ((data.name_fr == "") && (data.name_en == "")){
        if (language == "fr"){
            createError("Merci de compléter au moins un des deux champs");
        }
        else{
            createError("Please fill-in at least one of the two fields");
        }
        return false;
    }

    $.ajax({
        type: "POST",
        url: my_url,
        data: data,
        error: function(answer, code) {
            showError(anwser);
        },
        success: function(answer){
            $("#create_status_beehouse").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });

    return false;
}


function redirect_create_apiary(){
    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/apiary/create";
    let language = $("html").attr("lang");
    let check;

    if (language == "fr"){
        check = confirm("Vous allez être redirigé vers la page de création de rucher")
    }
    else{
        check = confirm("You will be redirected to the apiary creation page")
    }
    
    if (check){
        window.location = my_url;
    }
}


function createNewBeehouse(){
    let data = {
        name: $("#beehouse_name").val(),
        date: $('#beehouse_birthday').val(),
        status: $("#beehouse_status").val(),
        apiary: $("#beehouse_apiary").val(),
        owner: $("#beehouse_owner").val(),
        health: $("#beehouse_health").val()
    };

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/beehouse/create";

    $.ajax({
        type: "POST",
        url: my_url,
        dataType: "json",
        data: data,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            showSuccess(answer);
            window.location = root_path + "/beehouse/index";
        }
    });
}

