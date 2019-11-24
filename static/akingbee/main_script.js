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
    let protocol = window.location.protocol;
    let root = window.location.hostname;
    let pathname = window.location.pathname;
    let port = window.location.port;

    // check this is working with a hidden port (http or https)
    // I implemented this specifically for flask and port 5000
    let url = protocol + "//" + root;
    if (port) {
        url = url + ":" + port
    }
    url = url + pathname;


    // Highlight of the top menu
    let menu = document.getElementById("main_menu");
    if (menu) {
        let buttons = menu.getElementsByClassName("nav-link");
        for (let i = 0; i < buttons.length; i++) {
            if (url.includes(buttons[i].href)) {
                buttons[i].className += " active";
                break;
            }
        }
    }

    // Highlight of the left menu
    let submenu = document.getElementById("sidebar-menu");
    if (submenu) {
        let subbuttons = submenu.getElementsByClassName("nav-link sub");
        for (let i = 0; i < subbuttons.length; i++) {
            if (subbuttons[i].href == url) {
                subbuttons[i].className += " active";
                break;
            }
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

function missing_field() {
    if (LANGUAGE == "fr"){
        createError("Certains champs ne sont pas remplis !");
    }
    else{
        createError("Some fields are not filled in !");
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
    $("#hive_birthday").val(new Date().toDateInputValue());
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
