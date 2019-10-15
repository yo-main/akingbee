function new_honey_type(){
    let value = $("#honey_value").val();
    let my_url = get_full_url("/honey_type");

    if (value == ""){
        field_name_not_provided_error();
    }
    else{
        $.ajax({
            type: "POST",
            url: my_url,
            data: {"value": value},
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
    let value = $("#status_value").val();
    let my_url = get_full_url("/apiary_status");

    if (value == ""){
        field_name_not_provided_error();
    }
    else{
        $.ajax({
            type: "POST",
            url: my_url,
            data: {"value": value},
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


function create_new_apiary(){
    let data = {
        name: $("#apiary_name").val(),
        location: $('#apiary_location').val(),
        birthday: $("#apiary_birthday").val(),
        status: $("#apiary_status").val(),
        honey_type: $("#apiary_honey_type").val(),
    };

    let my_url = get_full_url("/apiary");

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
            window.location.reload();
        }
    });
}
