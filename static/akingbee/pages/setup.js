function show_modal_new_data(button){
    $("#modal_new_data").modal("show");
}

function show_modal_data_edit(button){
    let data = $(button).closest("tr").children("td.data_td").text();
    let data_id = button.getAttribute("data_id");

    $("#modal_edit_data").attr("data_id", data_id);
    $("#edit_data_name").val(data);

    $("#modal_edit_data").modal("show");
}



function show_delete_data(button){
    let confirm;
    let id = button.getAttribute("data_id");

    let my_url = window.location.href;

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
            data: {id: id},
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



function create_data(){
    let value = $("#new_data_name").val();
    send_data(value, "", "POST");
}

function edit_data(){
    let id = $("#modal_edit_data").attr("data_id");
    let value = $("#edit_data_name").val();
    send_data(value, id, "PUT");
}

function send_data(value, id, method) {

    let my_url = window.location.href;

    if (method != "DEL" && !value){
        missing_field();
        return false;
    }
    
    $.ajax({
        url: my_url,
        type: method,
        data: {data: value, id: id},
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            showSuccess(answer);
            window.location.reload();
        }
    });
}



