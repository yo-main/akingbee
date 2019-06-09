function modal_data_submit(button){
    $("#submit_data").modal("show");
    let dataId = button.name.substring(3);
    $("#data_id").attr("name", dataId);
}



function modal_data_edit(button){
    let language = $("html").attr("lang");
    
    $("#edit_data").modal("show");

    let data = $(button).closest("tr").children("td.data_td").text();
    let dataId = button.name.substring(3);

    $("#data_id").attr("name", dataId);
    $("#data_name_modal").val(data);
}



function delete_data(button){
    let language = $("html").attr("lang");
    let confirm;
    let data = {
        dataId: button.name.substring(3),
        source: window.location.pathname
    }

    let my_url = get_full_url("/setup/delete");

    if (language == "fr"){
        confirm = window.confirm("Supprimer cette entrée ?");
    }
    else{
        confirm = window.confirm("Delete this entry ?");
    }

    if (confirm){
        $.ajax({
            url: my_url,
            type: "POST",
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
}



function submit_modal_data_submit(){
    let language = $("html").attr("lang");
    let data = {
        fr: $("#submit_name_modal").val(),
        en: $("#submit_name_modal").val(),
        source: window.location.pathname
    }

    if (data.en == undefined){
        data.en = "";
    }

    let my_url = get_full_url("/setup/submit");

    if ((data.fr == "") && (data.en == "")){
        if (language == "fr"){
            createError("Merci de remplir les champs");
        }
        else{
            createError("Please fill-in the fields");
        }
        return false;
    }
    
    $.ajax({
        url: my_url,
        type: "POST",
        data: data,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            $("#submit_data").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });
}



function submit_modal_data_edit(){
    let language = $("html").attr("lang");
    let name = $("#data_name_modal").val();

    if (name == ""){
        if (language == "fr"){
            createError("Merci de remplir au moins un des deux champs");
        }
        else{
            createError("Please fill-in at least one of the two fields");
        }
        return false;
    }

    let data = {
        fr: name,
        en: name,
        dataId: $("#data_id").attr('name'),
        source: window.location.pathname
    }

    let my_url = get_full_url("/setup/update");

    $.ajax({
        type: "POST",
        url: my_url,
        data: data,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            $("#submit_action").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });
}

