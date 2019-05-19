function new_honey_type(){
    let data = {
        name_fr: $("#name_fr").val(),
        name_en: $("#name_en").val()
    };

    let language = $("html").attr("lang");
    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/apiary/create/new_honey_type";

    if ((data.name_fr == "") && (data.name_en == "")){
        if (language == "fr"){
            createError("Merci de compléter au moins un des deux champs");
        }
        else{
            createError("Please fill-in at least one of the two fields");
        }
    }
    else{
        $.ajax({
            type: "POST",
            url: my_url,
            data: data,
            error: function(answer, code){
                showError(answer);  
            },
            success: function(answer, code){
                $("#create_honey_type").modal("hide");
                showSuccess(answer);
                window.location.reload();
            }
        });
    }
}


function new_apiary_status(){
    let data = {
        name_fr: $("#status_fr").val(),
        name_en: $("#status_en").val()
    };

    let language = $("html").attr("lang");

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/apiary/create/new_apiary_status";

    if ((data.name_fr == "") && (data.name_en == "")){
        if (language == "fr"){
            createError("Merci de compléter au moins un des deux champs");
        }
        else{
            createError("Please fill-in at least one of the two fields");
        }
    }
    else{
        $.ajax({
            type: "POST",
            url: my_url,
            data: data,
            error: function(answer, code){
                showError(answer);  
            },
            success: function(answer, code){
                $("#create_apiary_status").modal("hide");
                showSuccess(answer);
                window.location.reload();
            }
        });
    }
}


function createNewApiary(){
    let data = {
        name: $("#apiary_name").val(),
        location: $('#apiary_location').val(),
        birthday: $("#apiary_birthday").val(),
        status: $("#apiary_status").val(),
        honey_type: $("#apiary_honey_type").val(),
    };

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/apiary/create";

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
            window.location = root_path + "/apiary/index";
        }
    });

    return false;
}
