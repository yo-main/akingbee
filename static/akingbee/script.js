const toastrOptions = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "positionClass": "toast-top-center",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOUt": 5000,
    "extendedTimeOut": 1000,
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}

var root_path = "/akingbee"


function menu_highlight() {
    let sidebar_menu = document.getElementById("sidebar-menu")
    let pathname = window.location.pathname;
	
    // Highlight as blue the current menu where a user is in
    if (pathname != "/setup"){
        if (sidebar_menu){
            // we get an array of our menu
            let btns = sidebar_menu.getElementsByClassName("nav-link sub");
            // in menu_nb is stored the id of the menu to highlight
            menuNb = $("#menu_nb").attr("name");
            // active colorizes the text in blue
            btns[menuNb].className += " active"; 
        }
    }
}

function menu_filter() {
    let pathname = window.location.pathname;

    if (pathname == "/hive"){
        filter_table_hive();
    }
    else if (pathname == "/apiary"){
        filter_table_apiary();
    }
}

function display_alerts() {
    let title = window.sessionStorage.getItem("msgSuccessTitle");
    let msg = window.sessionStorage.getItem("msgSuccessBody");

    if (msg){
            createSuccess(msg, title);
            window.sessionStorage.removeItem("msgSuccessTitle");
            window.sessionStorage.removeItem("msgSuccessBody");
    }
}

function set_active_language() {
    let language = $("html").attr("lang");
    if (language == "fr"){
        document.getElementById("userLanguage").selectedIndex = 0;
    }
    else{
        document.getElementById("userLanguage").selectedIndex = 1;
    }
}

function set_date_picker() {
    let language = $("html").attr("lang");
    if (language == "fr"){
        $.datepicker.setDefaults( $.datepicker.regional[ "fr" ] );
        $('[name="date"]').attr("placeholder", "jj/mm/aaaa");
    }
    else{    
        $.datepicker.setDefaults( $.datepicker.regional[ "" ] );
        $('[name="date"]').attr("placeholder", "mm/dd/yyyy");
    }

    $('[name="date"]').datepicker();
    
    $("#apiary_birthday").val(new Date().toDateInputValue());
    $("#hive_birthday").val(new Date().toDateInputValue());
}


$(document).ready(function() {
    set_active_language();
    menu_highlight();
    menu_filter();
    display_alerts();
    set_date_picker();
});


Date.prototype.toDateInputValue = (function() {
    // format the date to the input box from html
    // (DD/MM/YYYY or MM/DD/YYYY depending on the user language)
    let local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());

    let language = $("html").attr("lang");
    let dateString;
    
    if (language == "fr"){
        dateString = ("0" + local.getUTCDate()).slice(-2) + "/" +
                     ("0" + (local.getUTCMonth() + 1)).slice(-2) + "/" +
                     local.getFullYear();
    }
    else {
        dateString = ("0" + (local.getUTCMonth() + 1)).slice(-2) + "/" +
                     ("0" + local.getUTCDate()).slice(-2) + "/" +
                     local.getFullYear();
    }
    
    return dateString;
});


function createError(msg, title){
    toastr.options = toastrOptions;
    toastr["error"](msg, title);
}


function createSuccess(msg, title){
    toastr.options = toastrOptions;
    toastr["success"](msg, title);
}


function showMsg(response, answer_status){
    let language = $('html').attr("lang");
    let msg = response.message[language];
    let code = response.code;
    let result = data.responseJSON.result;

    if (answer_status == "success"){
        window.sessionStorage.setItem("msgSuccessTitle", msg.title[language]);
        window.sessionStorage.setItem("msgSuccessBody", msg.body[language]);
    }
    else if (answer_status == "error"){
        if (language == "fr"){
            createError(msg.fr, "Erreur #" + code);
        }
        else{
            createError(msg.en, "Error #" + code);
        }
    }
}


function changeLanguage(){
    //update the language upon edit on the language select box
    let data = {language: $("#userLanguage").val()};

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/language";
    $.ajax({
        type: "POST",
        url: my_url,
        data: data,
        success: function(){
            window.location.reload();
        }
    });
}


function forgot_password(){
    let myUrl = window.location.protocol + "//" + window.location.host + "/akingbee/reset_password";
    window.location = myUrl;
}


function validateRegisterForm(){
    let username = $("#username").val();
    let email = $("#email").val();
    let pwd1 = $("#password").val();
    let pwd2 = $("#passwordConfirmation").val();
    
    let language = $("html").attr("lang");

    if (username == '' || email == '' || pwd1 == '' || pwd2 == ''){
        if (language == "fr"){
            createError("Merci de remplir tous les champs");
        }
        else{
            createError("Please fill-in every fields");
        }

        return false;
    }
    
    if (pwd1 != pwd2){
        if (language == "fr"){
            createError("Les mots de passes ne sont pas identique");
        }
        else{
            createError("The passwords are not matching");
        }
        
        return false;
    }

    $.ajax({
        url: "registercheck",
        type: "POST",
        data: {username: username,
               email: email,
               pwd: pwd1},
        complete: function(answer){
            let result = answer.responseJSON.result;
            showMsg(answer);

            if (result == "success"){
                location = root_path + "/";
            }
        }
    });

    return false;   
}


function validateLogin(){
    let data = {
        username: $("#username").val(),
        password: $("#password").val()
    };
    
    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/login";
    
    $.ajax({
        type: "POST",
        url: my_url,
        data: data,
        complete: function(answer){
            let result = answer.responseJSON.result;
            showMsg(answer);

            if (result == "success"){
                location = root_path + "/";
            }
        }
    });

    return false;
}


function validateResetForm(){
    let username = $("#username").val();
    let pwd1 = $("#password").val();
    let pwd2 = $("#passwordConfirmation").val();
    
    let language = $("html").attr("lang");

    if (username == '' || pwd1 == '' || pwd2 == ''){
        return false;
    }

    if (pwd1 != pwd2){
        if (language == "fr"){
            createError("Les mots de passes ne sont pas identique");
        }
        else{
            createError("The passwords are not matching");
        }
        
        return false;
    }

    $.ajax({
        url: "reset_password",
        type: "POST",
        data: {username: username,
               pwd: pwd1},
        complete: function(answer){
            
            let result = answer.responseJSON.result;
            showMsg(answer);

            if (result == "success"){
                location = root_path + "/";
            }
        }
    });

    return false;   
}


function createNewHive(){
    let data = {
        name: $("#hive_name").val(),
        date: $('#hive_birthday').val(),
        status: $("#hive_status").val(),
        apiary: $("#hive_apiary").val(),
        owner: $("#hive_owner").val(),
        health: $("#hive_health").val()
    };

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/hive/create";

    $.ajax({
        type: "POST",
        url: my_url,
        dataType: "json",
        data: data,
        complete: function(answer){
            let result = answer.responseJSON.result;
            showMsg(answer);

            if (result == "success"){
                window.location = root_path + "/hive";
            }                    
        }
    });
}


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
            complete: function(answer){
                $("#create_honey_type").modal("hide");
				
				let result = answer.responseJSON.result;
				showMsg(answer);
                
				if (result == "success"){
					window.location.reload();
				} 
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
            complete: function(answer){
                $("#create_apiary_status").modal("hide");
				
				let result = answer.responseJSON.result;
				showMsg(answer);
                
				if (result == "success"){
					window.location.reload();
				}
            }
        });
    }
}


function new_owner(){
    let data = {owner: $("#owner_name").val()};
    let language = $("html").attr("lang");

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/hive/create/new_owner";

    if (data.owner == ""){
        if (language == "fr"){
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
        complete: function(answer){
            $("#create_owner").modal("hide");

            let result = answer.responseJSON.result;
            showMsg(answer);

            if (result == "success"){
                window.location.reload();
            }
        }
    });
}


function new_health(){
    let data = {
        name_fr: $("#health_name_fr").val(),
        name_en: $('#health_name_en').val()
    };

    let language = $('html').attr("lang");
    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/hive/create/new_health";

    if ((data.name_fr == "") && (data.name_en == "")){
        if (language == "fr"){
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
        complete: function(answer){
            $("#create_health").modal("hide");
            
            let result = answer.responseJSON.result;
            showMsg(answer);

            if (result == "success"){
                window.location.reload();
            }      
        }
    });
}


function new_status_hive(){
    let data = {
        name_fr: $("#status_hive_name_fr").val(),
        name_en: $('#status_hive_name_en').val()
    };

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/hive/create/new_hive_status";

    if ((data.name_fr == "") && (data.name_en == "")){
        if (language == "fr"){
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
        complete: function(answer){
            $("#create_status_hive").modal("hide");

            let result = answer.responseJSON.result;
            showMsg(answer);

            if (result == "success"){
                window.location.reload();
            }                     
        }
    });
}


function redirect_create_apiary(){
    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/apiary/create";
    let language = $("html").attr("lang");
    let check;

    if (language == "fr"){
        check = confirm("Vous allez être redirigé vers la page de création de rucher")
    }
    else{
        check = confirm("You will be redirected to the apiary creation page")
    }
    
    if (check){
        window.location = my_url;
    }
}


function filter_table_hive(){
    let apiary = $("#apiary_filter").val();
    let owner = $("#owner_filter").val();
    let health = $("#health_filter").val();
    let status = $("#status_filter").val();
    
    let table = document.getElementById("hive_table");
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


function modal_hive_edit(button){

    pName = window.location.pathname;
    let ruche_id;
    let my_url;

    if (pName == "/hive"){
        ruche_id = button.name.substring(3);
        my_url = window.location.protocol + "//" + window.location.host + "/akingbee/hive/get_hive_info";
    }
    else if (pName == "/hive"){
        let params = (new URL(document.location)).searchParams;
        ruche_id = params.get("bh");
        my_url = window.location.protocol + "//" + window.location.host + "/akingbee/hive/get_hive_info";
    }

    $.ajax({
        type: "POST",
        url: my_url,
        data: {bh_id: ruche_id},
        success: function(answer){
            $("#edit_hive").modal("show");
            
            $("#hive_name_modal").val(answer[0][0]);
            $("#apiary_name_modal").val(answer[0][1]).change();
            $("#owner_name_modal").val(answer[0][4]).change();
            $("#status_name_modal").val(answer[0][2]).change();

            $("#hive_id").attr("name", ruche_id);
            $("#hive_name_modal").attr("name", answer[0][0]);
            $("#apiary_name_modal").attr("name", answer[0][1]);
            $("#owner_name_modal").attr("name", answer[0][4]);
            $("#status_name_modal").attr("name", answer[0][2]);
        }
    });
}


function submit_hive_modal(){
    let new_hive = $("#hive_name_modal").val();
    let new_apiary = $("#apiary_name_modal").val();
    let new_owner = $("#owner_name_modal").val();
    let new_status = $("#status_name_modal").val();

    let hive = $("#hive_name_modal").attr("name");
    let apiary = $("#apiary_name_modal").attr("name");
    let owner = $("#owner_name_modal").attr("name");
    let status = $("#status_name_modal").attr("name");

    let bh_id = $("#hive_id").attr("name");
    let to_change = new Object();
    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/hive/submit_hive_info";
    let language = $("html").attr("lang");

    to_change.bh_id = bh_id;

    if (new_apiary != apiary){
        to_change.apiary = new_apiary;
    }

    if (new_hive != hive){
        to_change.hive = new_hive;
    }

    if (new_owner != owner){
        to_change.owner = new_owner;
    }

    if (new_status != status){
        to_change.status = new_status;
    }
    
    if (Object.keys(to_change).length > 1){
        $.ajax({
            type: "POST",
            url: my_url,
            data: to_change,
            complete: function(answer){
                $("#edit_hive").modal("hide");
            
                let result = answer.responseJSON.result;
                showMsg(answer);

                if (result == "success"){
                    window.location.reload();
                }
            }
        });
    }
}


function modal_comment(button){

    pName = window.location.pathname;
    let bh_id;
    let bh_name;

    if (pName == "/hive"){
        bh_id = button.name.substring(3);
        bh_name = $(button).closest("tr").children("td.name_td").text();
    }
    else if (pName == "/hive"){
        let params = (new URL(document.location)).searchParams;
        bh_id = params.get("bh");
        bh_name = $(button).attr("name");
    }

    $("#submit_comment").modal("show");

    $("#comment_name").val(bh_name);
    $("#comment_name").attr("name", bh_id);
    $("#comment_date").val(new Date().toDateInputValue());
}


function submit_comment_modal(){
    let data = {
        date: $("#comment_date").val(),
        health: $("#comment_health").val(),
        comment: $("#comment_comment").val(),
        bh_id: $("#comment_name").attr("name")
    }

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/hive/submit_comment_modal";
    
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
        complete: function(answer){
            $("#submit_comment").modal("hide");

            let result = answer.responseJSON.result;
            showMsg(answer);

            if (result == "success"){
                window.location.reload();
            }
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
    else if (pName == "/hive"){
        let params = (new URL(document.location)).searchParams;
        bh_id = params.get("bh");
        bh_name = $(button).attr("name");
    }

    $("#submit_action").modal("show");

    $("#action_name").val(bh_name);
    $("#action_name").attr("name", bh_id);
    $("#action_date").val(new Date().toDateInputValue());
}


function submit_action_modal(){
    let data = {
        date: $("#action_date").val(),
        comment: $("#action_comment").val(),
        bh_id: $("#action_name").attr("name"),
        deadline: $("#action_deadline").val(),
        action_type: $("#action_type").val()
    };

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/hive/submit_action_modal";

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
        complete: function(answer){
            $("#submit_action").modal("hide");
            
            let result = answer.responseJSON.result;
            showMsg(answer);

            if (result == "success"){
                window.location.reload();
            }
        }
    });
}


function select_hive(button){
    bh_id = button.name.substring(3);
    myUrl = window.location.protocol + "//" + window.location.host + "/akingbee/hive?bh=" + bh_id;
    window.location = myUrl;
}


function arrowAction(way){
    let params = (new URL(document.location)).searchParams;
    let bh_id = params.get("bh");
    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/hive/select";

    $.ajax({
        type: "POST",
        url: my_url,
        data: {
            bh_id: bh_id,
            way: way
        },
        success: function(answer){
            window.location = answer;
        }
    });
}


function modal_solve_action(button){
    $("#solve_action").modal("show");
    let name = button.title;
    $("#action_name_done").val(name)
    $("#action_name_done").attr("name", button.name);
}


function submit_solve_action_modal(){
    let data = {
        name: $("#action_name_done").val(),
        comment: $("#action_comment_done").val(),
        ac_id: $("#action_name_done").attr("name"),
        date: $("#action_date_done").val()
    }

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/hive/submit_solve_action_modal";
    let language = $("html").attr("lang");

    $.ajax({
        type: "POST",
        url: my_url,
        data: data,
        complete: function(answer){
            $("#submit_action").modal("hide");

            let result = answer.responseJSON.result;
            showMsg(answer);

            if (result == "success"){
                window.location.reload();
            }
        }
    });
}


function modal_edit_comment(button){
    let language = $('html').attr("lang");

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


function submit_edit_comment_modal(){
    let data = {
        comment: $("#comment_comment_edit").val(),
        cm_id: $("#comment_comment_edit").attr("name"),
        health: $("#comment_health_edit").find("option:selected").attr('title'),
        date: $("#comment_date_edit").val()
    }
    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/hive/submit_edit_comment_modal";

    $.ajax({
        type: "POST",
        url: my_url,
        data: data,
        complete: function(answer){
            $("#submit_action").modal("hide");

            let result = answer.responseJSON.result;
            showMsg(answer);

            if (result == "success"){
                window.location.reload();
            }
        }
    });
}


function del_comment(button){
    let language = $("html").attr("lang");
    let confirm;
    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/hive/delete_comment";

    if (language == "fr"){
        confirm = window.confirm("Etes-vous sur de vouloir supprimer ce commentaire ?");
    }
    else{
        confirm = window.confirm ("Delete this comment ?");
    }

    if (confirm){
        let cm_id = button.name.substring(3);

        $.ajax({
            type: "POST",
            url: my_url,
            data: {cm_id: cm_id},
            complete: function(answer){
                $("#submit_action").modal("hide");

                let result = answer.responseJSON.result;
                showMsg(answer);

                if (result == "success"){
                    window.location.reload();
                }
            }
        });
    }
}


function modal_data_edit(button){
    let language = $("html").attr("lang");
    
    $("#edit_data").modal("show");

    let dataFr = $(button).closest("tr").children("td.data_fr_td").text();
    let dataEn = $(button).closest("tr").children("td.data_en_td").text();
    let dataId = button.name.substring(3);

    $("#data_fr_id").attr("name", dataId);
    $("#data_name_fr_modal").val(dataFr);
    $("#data_name_en_modal").val(dataEn);
}


function submit_modal_data_edit(){
    let data = {
        fr: $("#data_name_fr_modal").val(),
        en: $("#data_name_en_modal").val(),
        dataId: $("#data_fr_id").attr('name'),
        source: window.location.pathname
    }

    if (data.en == undefined){
        data.en = "";
    }

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/setup/update";

    if ((data.fr == "") && (data.en == "")){
        if (language == "fr"){
            createError("Merci de remplir au moins un des deux champs");
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
        complete: function(answer){
            $("#submit_action").modal("hide");
            
            let result = answer.responseJSON.result;
            showMsg(answer);

            if (result == "success"){
                window.location.reload();
            }
        }
    });
}


function delete_data(button){
    let language = $("html").attr("lang");
    let confirm;
    let data = {
        dataId: button.name.substring(3),
        source: window.location.pathname
    }

    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/setup/delete";

    if (language == "fr"){
        confirm = window.confirm("Etes-vous sur de vouloir supprimer cette entrée ?");
    }
    else{
        confirm = window.confirm("Delete this entry ?");
    }

    if (confirm){
        $.ajax({
            type: "POST",
            url: my_url,
            data: data,
            complete: function(answer){

                let result = answer.responseJSON.result;
                showMsg(answer);

                if (result == "success"){
                    window.location.reload();
                }
            }
        });
    }
}


function modal_data_submit(button){
    $("#submit_data").modal("show");
    let dataId = button.name.substring(3);
    $("#data_en_id").attr("name", dataId);
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
        complete: function(answer){
            $("#submit_data").modal("hide");

            let result = answer.responseJSON.result;
            showMsg(answer);

            if (result == "success"){
                window.location.reload();
            }
		}
	});
}


function filter_table_apiary(){
    let location = $("#location_filter").val();
    let status = $("#status_filter").val();
    let honey = $("#honey_filter").val();
    
    let table = document.getElementById("apiary_table");
    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++){
        let td = tr[i].getElementsByTagName("td");
        let flag = 0;

        let location_td = td[1].innerText;
        let status_td = td[2].innerText;
        let honey_td = td[3].innerText;

        if(location){
            if (location != location_td){
                flag = 1;
            }
        }
        
        if(status){
            if (status != status_td){
                flag = 1;
            }
        }
        
        if(honey){
            if (honey != honey_td){
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


function modal_apiary_edit(button){
    let apiary_id = button.name.substring(5);
    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/apiary/get_apiary_info";

    $.ajax({
        type: "POST",
        url: my_url,
        data: {ap_id: apiary_id},
        success: function(answer){
            $("#edit_apiary").modal("show");
            
            $("#apiary_name_modal").val(answer[0][0]);
            $("#apiary_location_modal").val(answer[0][1]);
            $("#apiary_status_modal").val(answer[0][2]).change();
            $("#apiary_honey_modal").val(answer[0][3]).change();

            $("#apiary_id").attr("name", apiary_id);
            $("#apiary_name_modal").attr("name", answer[0][0]);
            $("#apiary_location_modal").attr("name", answer[0][1]);
            $("#apiary_status_modal").attr("name", answer[0][2]);
            $("#apiary_honey_modal").attr("name", answer[0][3]);
        }
    });
}


function submit_apiary_modal(){
    let new_name = $("#apiary_name_modal").val();
    let new_location = $("#apiary_location_modal").val();
    let new_status = $("#apiary_status_modal").val();
    let new_honey = $("#apiary_honey_modal").val();

    let name = $("#apiary_name_modal").attr("name");
    let location = $("#apiary_location_modal").attr("name");
    let status = $("#apiary_status_modal").attr("name");
    let honey = $("#apiary_honey_modal").attr("name");

    let ap_id = $("#apiary_id").attr("name");
    let to_change = new Object();
    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/apiary/submit_apiary_info";
    let language = $("html").attr("lang");

    to_change.ap_id = ap_id;

    if (new_name != name){
        to_change.name = new_name;
    }

    if (new_location != location){
        to_change.location = new_location;
    }

    if (new_status != status){
        to_change.status = new_status;
    }

    if (new_honey != honey){
        to_change.honey = new_honey;
    }
    
    if (Object.keys(to_change).length > 1){
        $.ajax({
            type: "POST",
            url: my_url,
            data: to_change,
            complete: function(answer){
                $("#edit_apiary").modal("hide");

                let result = answer.responseJSON.result;
                showMsg(answer);

                if (result == "success"){
                    window.location.reload();
                }
            }
        });
    }
}


function delete_apiary(button){
    let apiary_id = button.name.substring(5);
    let confirm;
    let my_url = window.location.protocol + "//" + window.location.host + "/akingbee/apiary/delete";

    if (language == "fr"){
        confirm = window.confirm("Supprimer ce rucher ?");
    }
    else{
        confirm = window.confirm ("Delete this apiary ?");
    }

    if (confirm){
        $.ajax({
            type: "POST",
            url: my_url,
            data: {ap_id: apiary_id},
            complete: function(answer){

                let result = answer.responseJSON.result;
                showMsg(answer);

                if (result == "success"){
                    window.location.reload();
                }
            }
        });
    }
}
