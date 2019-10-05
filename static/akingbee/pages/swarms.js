function arrowAction(way){
    let pathname = window.location.pathname;
    let args = pathname.split("/");

    let swarm_id = args[2];
    let my_url = get_full_url("/swarm/select");

    $.ajax({
        type: "POST",
        url: my_url,
        data: {
            swarm_id: swarm_id,
            way: way
        },
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            window.location = get_full_url(answer);
        }
    });
}


function modal_action(button){

    let bh_name;
    let bh_id;

    pName = window.location.pathname;

    if (pName == "/swarm"){
        swarm_id = button.name.substring(3);
        swarm_name = $(button).closest("tr").children("td.name_td").text();
    }
    else if (pName.includes("/swarm/")){
        let pathname = window.location.pathname;
        let args = pathname.split("/");
        swarm_id = args[2];
        swarm_name = $(button).attr("name");
    }

    $("#submit_action").modal("show");

    $("#action_name").val(swarm_name);
    $("#action_name").attr("name", swarm_id);
    $("#action_date").val(new Date().toDateInputValue());
}


function modal_solve_action(button){
    $("#solve_action").modal("show");
    let name = button.title;
    $("#action_name_done").val(name)
    $("#action_name_done").attr("name", button.name);
}


function filter_table_hive_details(){
    let source = $("#source_filter").val();
    let apiary = $("#apiary_filter").val();
    let condition = $("#condition_filter").val();

    let table = document.getElementById("comment_table");
    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++){
        let td = tr[i].getElementsByTagName("td");
        let flag = 0; 

        let source_td = td[1].innerText;
        let apiary_td = td[2].innerText;
        let condition_td = td[3].innerText;

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


function modal_edit_comment(button){

    $("#edit_comment_bh").modal("show");

    let date = $(button).closest("tr").children("td.date_cm").text();
    let health = $(button).closest("tr").children("td.health_cm").text();
    let comment = $(button).closest("tr").children("td.comm_cm").text();
    let cm_id = button.name.substring(3);
    
    $("#comment_comment_edit").attr('name', cm_id);
    $("#comment_date_edit").val(date);
    $("#comment_comment_edit").val(comment);
    $("#comment_health_edit").val(health).change();
}


function del_comment(button){
    let confirmation;
    let my_url = get_full_url("/hive/delete_comment");

    if (LANGUAGE == "fr"){
        confirmation = window.confirm("Etes-vous sur de vouloir supprimer ce commentaire ?");
    }
    else{
        confirmation = window.confirm("Delete this comment ?");
    }

    if (confirmation){
        let cm_id = button.name.substring(3);

        $.ajax({
            type: "POST",
            url: my_url,
            data: {cm_id: cm_id},
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


function submit_solve_action_modal(){
    let data = {
        name: $("#action_name_done").val(),
        comment: $("#action_comment_done").val(),
        ac_id: $("#action_name_done").attr("name"),
        date: $("#action_date_done").val()
    }

    let my_url = get_full_url("/hive/submit_solve_action_modal");

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


function submit_edit_comment_modal(){
    let data = {
        comment: $("#comment_comment_edit").val(),
        cm_id: $("#comment_comment_edit").attr("name"),
        health: $("#comment_health_edit").find("option:selected").attr('title'),
        date: $("#comment_date_edit").val()
    }
    let my_url = get_full_url("/hive/submit_edit_comment_modal");

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


function new_swarm_health(){
    let data = {
        name_fr: $("#swarm_health_name_fr").val(),
        name_en: $('#swarm_health_name_en').val()
    };

    let my_url = get_full_url("/swarm/create/new_health");

    if ((data.name_fr == "") && (data.name_en == "")){
        if (LANGUAGE == "fr"){
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
            $("#create_swarm_health").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });

    return false;
}


function redirect_create_hive(){
    let my_url = get_full_url("/hive/create");
    let confirmation;

    if (LANGUAGE == "fr"){
        confirmation = window.confirm("Vous allez être redirigé vers la page de création d'une ruche")
    }
    else{
        confirmation = window.confirm("You will be redirected to the hive creation page")
    }
    
    if (confirmation){
        window.location = my_url;
    }
}


function createNewSwarm(){
    let data = {
        "name": $("#swarm_name").val(),
        "birthday": $('#swarm_birthday').val(),
        "hive": $('#swarm_hive').val(),
        "health": $("#swarm_health").val()
    };

    for (attr in data) {
        if (data[attr] == "") {
            if (LANGUAGE == "fr") {
                createError("Veuillez renseigner tous les détails");
            }
            else {
                createError("Fill in all the details");
            }
            return false;
        }
    }

    let my_url = get_full_url("/swarm/create");

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
            window.location = get_full_url("/swarm");
        }
    });
}


function select_swarm(button){
    swarm_id = button.name.substring(3);
    myUrl = get_full_url("/swarm/" + swarm_id);
    window.location = myUrl;
}

function submit_action_modal(){

    let data = {
        date: $("#action_date").val(),
        comment: $("#action_comment").val(),
        bh_id: $("#action_name").attr("name"),
        deadline: $("#action_deadline").val(),
        action_type: $("#action_type").val()
    };

    let my_url = get_full_url("/hive/submit_action_modal");

    if ((data.action_type == "") || (data.date == "")){
        if (LANGUAGE == "fr"){
            createError("Merci de remplir tous les champs", "Titre");
        }
        else{
            createError("Please fill-in all the fields", "Title");
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
            $("#submit_action").modal("hide");
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

function modal_comment(button){

    let pName = window.location.pathname;
    let swarm_id;
    let swarm_name;

    if (pName == "/swarm"){
        swarm_id = button.name.substring(3);
        swarm_name = $(button).closest("tr").children("td.name_td").text();
    }
    else if (pName.includes("/swarm/")){
        let pathname = window.location.pathname;
        let args = pathname.split("/");
        bh_id = args[2];
        bh_name = $(button).attr("name");
    }

    $("#submit_comment").modal("show");

    $("#comment_name").val(swarm_name);
    $("#comment_name").attr("name", swarm_id);
    $("#comment_date").val(new Date().toDateInputValue());
}


function modal_swarm_edit(button){

    let pName = window.location.pathname;
    let swarm_id;
    let my_url;

    my_url = get_full_url("/swarm/get_swarm_info");
    
    if (pName.includes("/swarm/")){
        swarm_id = pName.split("/")[2];
    }
    else if (pName.includes("/swarm")){
        swarm_id = button.name.substring(6);
    }

    $.ajax({
        type: "POST",
        url: my_url,
        data: {swarm_id: swarm_id},
        error: function (answer, code){
            showError(answer);
        },
        success: function(answer, code){
            let swarm = answer;
            $("#edit_swarm").modal("show");
    
            $("#swarm_id").attr("name", swarm_id);
            $("#swarm_name_modal").attr("name", swarm.name);
            $("#swarm_health_modal").attr("name", swarm.health_id);
            $("#swarm_hive_modal").attr("name", swarm.hive_id);

            $("#swarm_name_modal").val(swarm.name);
            $("#swarm_health_modal").val(swarm.health_id).change();
            $("#swarm_hive_modal").val(swarm.hive_id).change();
        }
    });
}


function filter_table_swarm(){
    let health = $("#health_filter").val();
    
    let table = document.getElementById("swarm_table");
    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++){
        let td = tr[i].getElementsByTagName("td");
        let flag = 0; 

        let health_td = td[2].innerText;

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


function submit_swarm_modal(){
    let new_name = $("#swarm_name_modal").val();
    let new_hive = $("#swarm_hive_modal").val();
    let new_health = $("#swarm_health_modal").val();

    let name = $("#swarm_name_modal").attr("name");
    let hive = $("#swarm_hive_modal").attr("name");
    let health = $("#swarm_health_modal").attr("name");

    let swarm_id = $("#swarm_id").attr("name");

    let to_change = new Object();
    let my_url = get_full_url("/swarm/submit_swarm_info");

    to_change.swarm_id = swarm_id;
    to_change.name = new_name;
    to_change.hive = new_hive;
    to_change.health = new_health;
    
    if (Object.keys(to_change).length > 1){
        $.ajax({
            type: "POST",
            url: my_url,
            data: to_change,
            error: function(answer, code){
                showError(answer);
            },
            success: function(answer, code){
                $("#edit_swarm").modal("hide");
                showSuccess(answer);
                window.location.reload();
            }
        });
    }
}


function submit_comment_modal(){
    let data = {
        date: $("#comment_date").val(),
        health: $("#comment_health").val(),
        comment: $("#comment_comment").val(),
        swarm_id: $("#comment_name").attr("name")
    }

    let my_url = get_full_url("/swarm/submit_comment_modal");
    
    if ((data.comment == "") || (data.health == "")){
        if (LANGUAGE == "fr"){
            createError("Merci de remplir tous les champs");
        }
        else{
            createError("Please fill-in all the fields");
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
            $("#submit_comment").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });
}


function delete_swarm(){
    let params = (new URL(document.location)).searchParams;
    let swarm_id = params.get("swarm");
    let url = get_full_url("/swarm/delete");

    let data = {"swarm_id": swarm_id};

    if (LANGUAGE == "fr"){
        confirmation = window.confirm("Supprimer cet essaim ?");
    }
    else{
        confirmation = window.confirm("Delete this swarm ?");
    }

    if (confirmation){
	$.ajax({
	    type: "POST",
	    url: url,
	    data: data,
	    error: function(answer, code){
		showError(answer);
	    },
	    success: function(answer, code){
		showSuccess(answer);
		window.location = get_full_url("/swarm");
	    }
	});
    };
}


