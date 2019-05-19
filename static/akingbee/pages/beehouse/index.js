
function select_beehouse(button){
    bh_id = button.name.substring(3);
    myUrl = window.location.protocol + "//" + window.location.host + "/akingbee/beehouse?bh=" + bh_id;
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

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/beehouse/index/submit_action_modal";

    if ((data.action_type == "") || (data.date == "")){
        if (language == "fr"){
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
            $("#submit_action").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });
}


function modal_action(button){

    let bh_name;
    let bh_id;

    pName = window.location.pathname;

    if (pName == "/beehouse/index"){
        bh_id = button.name.substring(3);
        bh_name = $(button).closest("tr").children("td.name_td").text();
    }
    else if (pName == "/beehouse"){
        let params = (new URL(document.location)).searchParams;
        bh_id = params.get("bh");
        bh_name = $(button).attr("name");
    }

    $("#submit_action").modal("show");

    $("#action_name").val(bh_name);
    $("#action_name").attr("name", bh_id);
    $("#action_date").val(new Date().toDateInputValue());
}


function submit_modal_data_submit(){
    let language = $("html").attr("lang");
    let data = {
        fr: $("#submit_name_fr_modal").val(),
        en: $("#submit_name_en_modal").val(),
        source: window.location.pathname
    }

    if (data.en == undefined){
        data.en = "";
    }

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/setup/submit";

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

    if (pName.includes("/beehouse/index")){
        bh_id = button.name.substring(3);
        bh_name = $(button).closest("tr").children("td.name_td").text();
    }
    else if (pName.includes("/beehouse")){
        let params = (new URL(document.location)).searchParams;
        bh_id = params.get("bh");
        bh_name = $(button).attr("name");
    }

    $("#submit_comment").modal("show");

    $("#comment_name").val(bh_name);
    $("#comment_name").attr("name", bh_id);
    $("#comment_date").val(new Date().toDateInputValue());
}



function modal_beehouse_edit(button){

    let pName = window.location.pathname;
    let ruche_id;
    let my_url;
    let language = $("html").attr("lang");

    my_url = window.location.protocol + "//" + window.location.host + "/akingbee/beehouse/index/get_beehouse_info";

    if (pName.includes("/beehouse/index")){
        ruche_id = button.name.substring(3);
    }
    else if (pName.includes("/beehouse")){
        let params = (new URL(document.location)).searchParams;
        ruche_id = params.get("bh");
    }

    $.ajax({
        type: "POST",
        url: my_url,
        data: {bh_id: ruche_id},
        error: function (answer, code){
            showError(answer);
        },
        success: function(answer, code){
            let beehouse = answer;
            $("#edit_beehouse").modal("show");
    
            $("#beehouse_id").attr("name", ruche_id);
            $("#beehouse_name_modal").attr("name", beehouse.name);
            $("#apiary_name_modal").attr("name", beehouse.apiary);
            $("#owner_name_modal").attr("name", beehouse.owner);
            $("#status_name_modal").attr("name", beehouse.status);
            
            $("#beehouse_name_modal").val(beehouse.name);
            $("#apiary_name_modal").val(beehouse.apiary).change();
            $("#owner_name_modal").val(beehouse.owner).change();
            $("#status_name_modal").val(beehouse.status).change();
        }
    });
}


function filter_table_beehouse(){
    let apiary = $("#apiary_filter").val();
    let owner = $("#owner_filter").val();
    let health = $("#health_filter").val();
    let status = $("#status_filter").val();
    
    let table = document.getElementById("beehouse_table");
    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++){
        let td = tr[i].getElementsByTagName("td");
        let flag = 0; 

        let apiary_td = td[1].innerText;
        let health_td = td[2].innerText;
        let owner_td = td[3].innerText;
        let status_td = td[4].innerText;

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
        
        if(health){
            if (health != health_td){
                flag = 1;
            }
        }
        
        if(status){
            if (status != status_td){
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




function submit_beehouse_modal(){
    let new_beehouse = $("#beehouse_name_modal").val();
    let new_apiary = $("#apiary_name_modal").val();
    let new_owner = $("#owner_name_modal").val();
    let new_status = $("#status_name_modal").val();

    let beehouse = $("#beehouse_name_modal").attr("name");
    let apiary = $("#apiary_name_modal").attr("name");
    let owner = $("#owner_name_modal").attr("name");
    let status = $("#status_name_modal").attr("name");

    let bh_id = $("#beehouse_id").attr("name");
    let to_change = new Object();
    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/beehouse/index/submit_beehouse_info";
    let language = $("html").attr("lang");

    to_change.bh_id = bh_id;
    to_change.apiary = new_apiary;
    to_change.beehouse = new_beehouse;
    to_change.owner = new_owner;
    to_change.status = new_status;
    
    if (Object.keys(to_change).length > 1){
        $.ajax({
            type: "POST",
            url: my_url,
            data: to_change,
            error: function(answer, code){
                showError(answer);
            },
            success: function(answer, code){
                $("#edit_beehouse").modal("hide");
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

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/beehouse/index/submit_comment_modal";
    
    if ((data.comment == "") || (data.health == "")){
        if (language == "fr"){
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


