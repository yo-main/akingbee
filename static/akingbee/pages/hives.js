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

        if (apiary && apiary != apiary_td){
            flag = 1;
        } else if(source && source != source_td){
            flag = 1;
        } else if(health && health != health_td){
            flag = 1;
        }

        if (flag == 1){
            tr[i].style.display = "none";
        }
        else{
            tr[i].style.display = "";
        }
    }
}


function del_comment(comment_id){
    let confirmation;
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
                showSuccess(answer);
                window.location.reload();
            }
        });
    }
}


function modal_solve_event(event_id, title){
    $("#modal_solve_event").modal("show");
    $("#solve_event_hive_id").val(event_id);
    $("#solve_event_name").val(title);
}


$("#solve-event-form").submit( function(event) {
    event.preventDefault();

    let event_id = $("#solve_event_hive_id").val();
    let my_url = get_full_url("/api/event/" + event_id);

    let data = {
        name: $("#solve_event_name").val(),
        date: $("#solve_event_date").val(),
        description: $("#solve_event_comment").val(),
    }

    $.ajax({
        type: "PUT",
        url: my_url,
        data: data,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            showSuccess(answer);
            window.location.reload();
        }
    });
});


$("#new-hive-condition-form").submit( function(event) {
    event.preventDefault();

    let my_url = get_full_url("/setup/hive/conditions");
    let name = $("#hive_condition_name").val()

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
});


$("#new-owner-form").submit( function(event) {
    event.preventDefault();

    let name = $("#owner_name").val();

    let my_url = get_full_url("/setup/hive/owner");

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
});


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

function show_modal_new_event(button){
    $("#new_event_date").val(new Date().toDateInputValue());
    $("#modal_new_event").modal("show");
}

$("#new-event-form").submit( function(event) {
    event.preventDefault();

    let data = {
        note: $("#new_event_note").val(),
        date: $("#new_event_date").val(),
        hive_id: $("#new_event_hive_id").val(),
        deadline: $("#new_event_deadline").val(),
        event_type: $("#new_event_type").val(),
    };

    let my_url = get_full_url("/api/event");

    $.ajax({
        type: "POST",
        url: my_url,
        data: data,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            showSuccess(answer);
            window.location.reload();
        }
    });
});


function show_modal_new_comment(){
    $("#new_comment_date").val(new Date().toDateInputValue());
    $("#modal_new_comment").modal("show");
}


$("#new-comment-form").submit( function(event) {
    event.preventDefault();

    let data = {
        date: $("#new_comment_date").val(),
        health: $("#new_comment_health").val(),
        comment: $("#new_comment_text").val(),
        hive_id: $("#new_comment_hive_id").val(),
        condition: $("#new_comment_condition").val(),
    }

    let my_url = get_full_url("/api/comment");

    $.ajax({
        type: "POST",
        url: my_url,
        data: data,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            showSuccess(answer);
            window.location.reload();
        }
    });
});


function show_modal_edit_comment(comment_id, button){
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


$("#edit-comment-form").submit( function(event) {
    event.preventDefault();

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
            $("#submit_event").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });
});


function show_modal_hive_edit(){
    $("#modal_edit_hive").modal("show");
}


$("#edit-hive-form").submit( function(event) {
    event.preventDefault();

    let hive_id = $("#hive_id_edit_modal").val();
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
});


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

        if (apiary && apiary != apiary_td){
            flag = 1;
        } else if(owner && owner != owner_td){
            flag = 1;
        } else if(condition && condition != condition_td){
            flag = 1;
        }

        if (flag == 1){
            tr[i].style.display = "none";
        } else{
            tr[i].style.display = "";
        }
    }
}


function delete_hive(hive_id){
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


$("#new-swarm-form").submit( function(event) {
    event.preventDefault();

    hive_id = $("#new_swarm_hive_id").val();

    let data = {
        "hive_id": hive_id,
        "swarm_health": $("#new_swarm_health").val()
    };

    let url = get_full_url("/api/swarm");

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
});


function show_create_swarm_modal(){
    $("#new_swarm_modal").modal("show");
}


function show_move_hive_modal(){
    $("#modal_move_hive").modal("show");
}

$("#move-hive-form").submit( function(event) {
    event.preventDefault();

    let hive_id = $("#hive_id_move_modal").val();
    let apiary_id = $("#apiary_name_move_modal").val();

    let url = get_full_url("/api/hive/" + hive_id + "/move/" + apiary_id);

    $.ajax({
        type: "POST",
        url: url,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            showSuccess(answer);
            window.location.reload();
        }
    });
});


function delete_swarm(hive_id){
    let url = get_full_url("/api/swarm");

    if (LANGUAGE == "fr"){
        confirmation = window.confirm("Supprimer l'essaim rattaché à cette ruche ?");
    }
    else{
        confirmation = window.confirm("Delete the swarm attached to this hive ?");
    }

    if (confirmation){
        $.ajax({
            type: "DEL",
            url: url,
            data: {hive_id: hive_id},
            error: function(answer, code){
                showError(answer);
            },
            success: function(answer, code){
                showSuccess(answer);
                window.location.reload();
            }
        });
    };
}

