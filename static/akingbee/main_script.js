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

var root_path = ""
var LANGUAGE = $("html").attr("lang");

$(document).ready(function() {
    set_active_language();
    menu_highlight();
    display_alerts();
    set_date_picker();
});


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

function get_full_url(path) {
    let out;
    out = window.location.protocol + "//" + window.location.host + root_path + path;
    return out;
}


function display_alerts() {
    let msg = window.sessionStorage.getItem("msgSuccessBody");
    let title = window.sessionStorage.getItem("msgSuccessTitle");

    if (msg){
            createSuccess(msg, title);
            window.sessionStorage.removeItem("msgSuccessBody");
            window.sessionStorage.removeItem("msgSuccessTitle");
    }
}


function createError(msg, title){
    toastr.options = toastrOptions;
    toastr["error"](msg, title);
}


function createSuccess(msg, title){
    toastr.options = toastrOptions;
    toastr["success"](msg, title);
}


function showError(response){
    let answer = response.responseJSON;
    if (answer == null){
        answer = [];
        answer['fr'] = [];
        answer['en'] = [];
        answer['fr']['message'] = "Une erreur interne s'est produite. Désolé :(";
        answer['en']['message'] = "An internal error happened. Sorry :(";
        answer.code = "999";
    };

    let content = answer[LANGUAGE];
    let code = answer.code;
    createError(content.message, content.title);
}


function showSuccess(response){
    let content = response[LANGUAGE];
    let code = response.code;
    window.sessionStorage.setItem("msgSuccessBody", content.message);
    window.sessionStorage.setItem("msgSuccessTitle", content.title);
}


function changeLanguage(){
    //update the language upon edit on the language select box
    let data = {'language': $("#userLanguage").val()};
    let my_url = get_full_url("/language");

    $.ajax({
        type: "POST",
        url: my_url,
        data: data,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            window.location.reload();
        }
    });
}

function set_active_language() {
    if (LANGUAGE == "fr"){
        document.getElementById("userLanguage").selectedIndex = 0;
    }
    else{
        document.getElementById("userLanguage").selectedIndex = 1;
    }
}

function set_date_picker() {
    if (LANGUAGE == 'fr'){
        $.datepicker.setDefaults( $.datepicker.regional[ "fr" ] );
        $('[date_picker="true"]').attr("placeholder", "jj/mm/aaaa");
    }else{    
        $.datepicker.setDefaults( $.datepicker.regional[ "" ] );
        $('[date_picker="true"]').attr("placeholder", "dd/mm/yyyy");
    }

    $('[date_picker="true"]').datepicker({dateFormat: 'dd/mm/yy'});

    $("#apiary_birthday").val(new Date().toDateInputValue());
    $("#beehouse_birthday").val(new Date().toDateInputValue());
}


Date.prototype.toDateInputValue = (function() {
    // format the date to the input box from html
    // (DD-MM-YYYY)
    let local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());

    let dateString;
    
    dateString = (("0" + local.getUTCDate()).slice(-2) + "/" +
                  ("0" + (local.getUTCMonth() + 1)).slice(-2) + "/" +
                  local.getFullYear());

    return dateString;
});
