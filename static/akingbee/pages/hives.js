function arrowAction(way){
    let pathname = window.location.pathname;
    let my_url = get_full_url("/api" + pathname + "/" + way);

    $.get({
        type: "GET",
        url: my_url,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            window.location = get_full_url(answer);
        }
    });
}


function filter_table_hive_details(){
    let source = $("#source_filter").val();
    let apiary = $("#apiary_filter").val();
    let health = $("#health_filter").val();

    let table = document.getElementById("comment_table");
    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++){
        let td = tr[i].getElementsByTagName("td");
        let flag = 0; 

        let source_td = td[1].innerText;
        let apiary_td = td[2].innerText;
        let health_td = td[3].innerText;

        if(apiary){
            if (apiary != apiary_td){
                flag = 1;
            }
        }
        
        if(source){
            if (source != source_td){
                flag = 1;
            }
        }
        
        if(health){
            if (health != health_td){
                flag = 1;
            }
        }
        
        if (flag == 1){
            tr[i].style.display = "none";
        }
        else{
            tr[i].style.display = "";
        }
    }
}



function del_comment(button){
    let confirmation;
    let comment_id = button.getAttribute("comment_id");
    let my_url = get_full_url("/api/comment/" + comment_id);

    if (LANGUAGE == "fr"){
        confirmation = window.confirm("Etes-vous sur de vouloir supprimer ce commentaire ?");
    }
    else{
        confirmation = window.confirm("Delete this comment ?");
    }

    if (confirmation){
        $.ajax({
            type: "DEL",
            url: my_url,
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
}


function modal_solve_action(button){
    $("#modal_solve_action").modal("show");
    $("#modal_solve_action").attr("action_id", button.getAttribute("action_id"));

    $("#solve_action_name").attr("name", button.title);
    $("#solve_action_name").val(button.title);
}


function submit_solve_action_modal(){
    let action_id = $("#modal_solve_action").attr("action_id");

    let data = {
        name: $("#solve_action_name").val(),
        date: $("#solve_action_date").val(),
        description: $("#solve_action_comment").val(),
    }

    let my_url = get_full_url("/api/action/" + action_id);

    $.ajax({
        type: "PUT",
        url: my_url,
        data: data,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            $("#modal_solve_action").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });
}


function new_hive_condition(){
    let my_url = get_full_url("/setup/hive/condition");
    let name = $("#hive_condition_name").val()

    if (name == ""){
        missing_field();
        return false;
    }

    $.ajax({
        type: "POST",
        url: my_url,
        data: {"data": name},
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            $("#create_hive_condition").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });
}


function new_owner(){
    let name = $("#owner_name").val();

    let my_url = get_full_url("/setup/hive/owner");

    if (name == ""){
        missing_field();
        return false;
    }

    $.ajax({
        type: "POST",
        url: my_url,
        data: {"data": name},
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            showSuccess(answer);
            window.location.reload();
        }
    });
}


function redirect_create_apiary(){
    let my_url = get_full_url("/apiary/create");
    let confirmation;

    if (LANGUAGE == "fr"){
        confirmation = window.confirm("Vous allez être redirigé vers la page de création de rucher")
    }
    else{
        confirmation = window.confirm("You will be redirected to the apiary creation page")
    }
    
    if (confirmation){
        window.location = my_url;
    }
}


function create_new_hive(){
    let data = {
        "name": $("#hive_name").val(),
        "date": $('#hive_birthday').val(),
        "apiary": $("#hive_apiary").val(),
        "owner": $("#hive_owner").val(),
        "hive_condition": $("#hive_condition").val(),
        "swarm_health": $("#hive_swarm_health").val()
    };

    for (attr in data) {
        if (data[attr] == "" && attr != "swarm_health") {
            if (LANGUAGE == "fr") {
                createError("Veuillez renseigner tous les détails");
            }
            else {
                createError("Fill in all the details");
            }
            return false;
        }
    }

    let my_url = get_full_url("/api/hive");

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
            window.location = get_full_url("/hive");
        }
    });
}


function select_hive(button){
    bh_id = button.name.substring(3);
    myUrl = get_full_url("/hive/" + bh_id);
    window.location = myUrl;
}

function show_modal_new_action(button){
    $("#new_action_date").val(new Date().toDateInputValue());
    $("#modal_new_action").modal("show");
}

function submit_new_action(){

    let data = {
        date: $("#new_action_date").val(),
        action_type: $("#new_action_type").val(),
        deadline: $("#new_action_deadline").val(),
        note: $("#new_action_note").val(),
        hive_id: $("#modal_new_action").attr("hive_id"),
    };

    let my_url = get_full_url("/api/action");

    if (!data.action_type || !data.date){
        missing_field();
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
            $("#modal_new_action").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });
}


function submit_modal_data_submit(){
    let data = {
        fr: $("#submit_name_fr_modal").val(),
        en: $("#submit_name_en_modal").val(),
        source: window.location.pathname
    }

    if (data.en == undefined){
        data.en = "";
    }

    let my_url = get_full_url("/setup/submit");

    if ((data.fr == "") && (data.en == "")){
        if (LANGUAGE == "fr"){
            createError("Merci de remplir les champs");
        }
        else{
            createError("Please fill-in the fields");
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
            $("#submit_data").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });
}

function show_modal_new_comment(){
    $("#new_comment_date").val(new Date().toDateInputValue());
    $("#modal_new_comment").modal("show");
}


function submit_new_comment(){
    let data = {
        date: $("#new_comment_date").val(),
        comment: $("#new_comment_text").val(),
        health: $("#new_comment_health").val(),
        condition: $("#new_comment_condition").val(),
        hive_id: $("#modal_new_comment").attr("hive_id")
    }

    let my_url = get_full_url("/api/comment");

    if (!data.comment || !data.date || !data.condition ||
        ($("#new_comment_health").is(":enabled") && !data.health)){
        missing_field();
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
            $("#submit_new_comment").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });
}


function show_modal_edit_comment(button){
    let comment_id = button.getAttribute("comment_id");

    let date = $(button).closest("tr").children("td.date_cm").text();
    let health = $(button).closest("tr").children("td.health_cm").attr("health_id");
    let condition = $(button).closest("tr").children("td.condition_cm").attr("condition_id");
    let comment = $(button).closest("tr").children("td.comm_cm").text();
    
    $("#edit_comment_date").val(date);
    $("#edit_comment_text").val(comment);
    $("#edit_comment_health").val(health).change();
    $("#edit_comment_condition").val(condition).change();

    $("#modal_edit_comment").attr('comment_id', comment_id);
    $("#modal_edit_comment").modal("show");
}


function edit_comment(){
    let comment_id = $("#modal_edit_comment").attr("comment_id");

    let data = {
        date: $("#edit_comment_date").val(),
        comment: $("#edit_comment_text").val(),
        health: $("#edit_comment_health").val(),
        condition: $("#edit_comment_condition").val(),
    }
    let my_url = get_full_url("/api/comment/" + comment_id);

    $.ajax({
        type: "PUT",
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


function show_modal_hive_edit(){
    $("#modal_edit_hive").modal("show");
}


function update_hive(){
    let hive_id = $("#modal_edit_hive").attr("hive_id");
    let my_url = get_full_url("/api/hive/" + hive_id);

    let old_owner = $("#owner_name_edit_modal").attr("old");
    let new_owner = $("#owner_name_edit_modal").val();

    let old_hive = $("#hive_name_edit_modal").attr("old");
    let new_hive = $("#hive_name_edit_modal").val();


    if (old_owner == new_owner && old_hive == new_hive) {
        if (LANGUAGE == "fr") {
            createError("Aucune valeur n'a été modifiée !");
        } else {
            createError("No value were modified !");
        }
        return false;
    }

    if (!new_owner || !new_hive) {
        missing_field()
        return false;        
    }
    
    data = {
        "owner": new_owner,
        "hive": new_hive,
    }

    $.ajax({
        type: "PUT",
        url: my_url,
        data: data,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            $("#modal_edit_hive").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });
}


function filter_table_hive(){
    let apiary = $("#apiary_filter").val();
    let owner = $("#owner_filter").val();
    let condition = $("#condition_filter").val();
    
    let table = document.getElementById("hive_table");
    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++){
        let td = tr[i].getElementsByTagName("td");
        let flag = 0; 

        let apiary_td = td[1].innerText;
        let owner_td = td[2].innerText;
        let condition_td = td[3].innerText;

        if(apiary){
            if (apiary != apiary_td){
                flag = 1;
            }
        }

        if(owner){
            if (owner != owner_td){
                flag = 1;
            }
        }
        
        if(condition){
            if (condition != condition_td){
                flag = 1;
            }
        }
        
        if (flag == 1){
            tr[i].style.display = "none";
        }
        else{
            tr[i].style.display = "";
        }
    }
}


function delete_hive(){
    let params = window.location.pathname;
    let hive_id = params.split("/")[2];
    let url = get_full_url("/api/hive/" + hive_id);

    if (LANGUAGE == "fr"){
        confirmation = window.confirm("Supprimer cette ruche ?");
    }
    else{
        confirmation = window.confirm("Delete this hive ?");
    }

    if (confirmation){
        $.ajax({
            type: "DEL",
            url: url,
            error: function(answer, code){
                showError(answer);
            },
            success: function(answer, code){
                showSuccess(answer);
                window.location = get_full_url("/hive");
            }
        });
    };
}


function attach_swarm_on_hive(button) {
    hive_id = $(button).attr("hive");
    
    let data = {
        "hive_id": hive_id,
        "swarm_health": $("#swarm_health").val()
    }
    let url = get_full_url("/swarm/create")

    $.ajax({
        type: "POST",
        url: url,
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

function show_swarm_create_modal(){
    let pName = window.location.pathname;
    $("#submit_new_swarm").modal("show");
    $("#comment_name").attr("name", bh_id);
}






