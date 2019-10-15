function arrowAction(way){
    let pathname = window.location.pathname;
    let args = pathname.split("/");

    let bh_id = args[2];
    let my_url = get_full_url("/hive/select");

    $.ajax({
        type: "POST",
        url: my_url,
        data: {
            bh_id: bh_id,
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

    if (pName == "/hive"){
        bh_id = button.name.substring(3);
        bh_name = $(button).closest("tr").children("td.name_td").text();
    }
    else if (pName.includes("/hive/")){
        let pathname = window.location.pathname;
        let args = pathname.split("/");
        bh_id = args[2];
        bh_name = $(button).attr("name");
    }

    $("#submit_action").modal("show");

    $("#action_name").val(bh_name);
    $("#action_name").attr("name", bh_id);
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


function modal_edit_comment(button){

    $("#edit_comment_bh").modal("show");

    let date = $(button).closest("tr").children("td.date_cm").text();
    let health = $(button).closest("tr").children("td.health_cm").text();
    let comment = $(button).closest("tr").children("td.comm_cm").text();
    let cm_id = button.name.substring(3);
    
    $("#comment_comment_edit").attr('name', cm_id);
    $("#comment_date_edit").val(date);
    $("#comment_comment_edit").val(comment);
    $("comment_condition_edit").val(condition).change();
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
        description: $("#action_description_done").val(),
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
        condition: $("#comment_condition_edit").find("option:selected").attr('title'),
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


function new_hive_condition(){
    let data = {
        name_fr: $("#hive_condition_name_fr").val(),
        name_en: $('#hive_condition_name_en').val()
    };

    let my_url = get_full_url("/hive/create/new_condition");

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
            $("#create_hive_condition").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });

    return false;
}


function new_owner(){
    let data = {owner: $("#owner_name").val()};

    let my_url = get_full_url("/hive/create/new_owner");

    if (data.owner == ""){
        if (LANGUAGE == "fr"){
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


function createNewHive(){
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

    let my_url = get_full_url("/hive");

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


function submit_action_modal(){

    let data = {
        date: $("#action_date").val(),
        description: $("#action_description").val(),
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
    let bh_id;
    let bh_name;

    if (pName == "/hive"){
        bh_id = button.name.substring(3);
        bh_name = $(button).closest("tr").children("td.name_td").text();
    }
    else if (pName.includes("/hive/")){
        let pathname = window.location.pathname;
        let args = pathname.split("/");
        bh_id = args[2];
        bh_name = $(button).attr("name");
    }

    $("#submit_comment").modal("show");

    $("#comment_name").val(bh_name);
    $("#comment_name").attr("name", bh_id);
    $("#comment_date").val(new Date().toDateInputValue());
}


function modal_hive_edit(button){

    let pName = window.location.pathname;
    let ruche_id;
    let my_url;

    my_url = get_full_url("/hive/get_hive_info");
    
    if (pName.includes("/hive/")){
        ruche_id = pName.split("/")[2];
    }
    else if (pName.includes("/hive")){
        ruche_id = button.name.substring(3);
    }

    $.ajax({
        type: "POST",
        url: my_url,
        data: {bh_id: ruche_id},
        error: function (answer, code){
            showError(answer);
        },
        success: function(answer, code){
            let hive = answer;
            $("#edit_hive").modal("show");
    
            $("#hive_id").attr("name", ruche_id);
            $("#hive_name_modal").attr("name", hive.name);
            $("#apiary_name_modal").attr("name", hive.apiary_id);
            $("#owner_name_modal").attr("name", hive.owner_id);
            $("#hive_condition_modal").attr("name", hive.condition_id);

            $("#hive_name_modal").val(hive.name);
            $("#apiary_name_modal").val(hive.apiary_id).change();
            $("#owner_name_modal").val(hive.owner_id).change();
            $("#hive_condition_modal").val(hive.condition_id).change();
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


function submit_hive_modal(){
    let new_hive = $("#hive_name_modal").val();
    let new_apiary = $("#apiary_name_modal").val();
    let new_owner = $("#owner_name_modal").val();
    let new_condition = $("#hive_condition_modal").val();

    let hive = $("#hive_name_modal").attr("name");
    let apiary = $("#apiary_name_modal").attr("name");
    let owner = $("#owner_name_modal").attr("name");
    let condition = $("#hive_condition_modal").attr("name");

    let bh_id = $("#hive_id").attr("name");
    let to_change = new Object();
    let my_url = get_full_url("/hive/submit_hive_info");

    to_change.bh_id = bh_id;
    to_change.apiary = new_apiary;
    to_change.hive = new_hive;
    to_change.owner = new_owner;
    to_change.condition = new_condition;
    
    if (Object.keys(to_change).length > 1){
        $.ajax({
            type: "POST",
            url: my_url,
            data: to_change,
            error: function(answer, code){
                showError(answer);
            },
            success: function(answer, code){
                $("#edit_hive").modal("hide");
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
        bh_id: $("#comment_name").attr("name")
    }

    let my_url = get_full_url("/hive/submit_comment_modal");
    
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


function delete_hive(){
    let params = (new URL(document.location)).searchParams;
    let bh_id = params.get("bh");
    let url = get_full_url("/hive/delete");

    let data = {"bh_id": bh_id};

    if (LANGUAGE == "fr"){
        confirmation = window.confirm("Supprimer cette ruche ?");
    }
    else{
        confirmation = window.confirm("Delete this hive ?");
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

function swarm_create_modal(){
    let pName = window.location.pathname;
    $("#submit_new_swarm").modal("show");
    $("#comment_name").attr("name", bh_id);
}






