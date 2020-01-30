function show_modal_new_data(button){
    $("#modal_new_data").modal("show");
}

function show_modal_data_edit(data_id, data_name){
    $("#modal_edit_data").attr("data_id", data_id);
    $("#edit_data_name").val(data_name);
    $("#modal_edit_data").modal("show");
}

function show_delete_data(data_id){
    let my_url = window.location.href;

    let confirm;
    if (LANGUAGE == "fr"){
        confirm = window.confirm("Supprimer cette entrée ?");
    }
    else{
        confirm = window.confirm("Delete this entry ?");
    }

    if (confirm){
        $.ajax({
            url: my_url,
            type: "DEL",
            data: {id: data_id},
            error: function(answer, code){
                showError(answer);
            },
            success: function(answer, code){
                showSuccess(answer);
                window.location.reload();
            }
        });
    }
}

$("#new-data-form").submit( function(event) {
    event.preventDefault();

    let data_name = $("#new_data_name").val();
    let my_url = window.location.href;

    $.ajax({
        type: "POST",
        url: my_url,
        data: {data: data_name},
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            showSuccess(answer);
            window.location.reload();
        }
    });
});

$("#edit-data-form").submit( function(event) {
    event.preventDefault();

    let my_url = window.location.href;

    let data_id = $("#modal_edit_data").attr("data_id");
    let data_name = $("#edit_data_name").val();

    $.ajax({
        type: "PUT",
        url: my_url,
        data: {data: data_name, id: data_id},
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            showSuccess(answer);
            window.location.reload();
        }
    });
});



