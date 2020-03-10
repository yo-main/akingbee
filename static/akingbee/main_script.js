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

var ROOT_PATH = ""
var LANGUAGE = $("html").attr("lang");
var QUILLS = {};

$(document).ready(function() {
    set_active_language();
    menu_highlight();
    display_alerts();
    set_date_picker();

    if ($("#new_comment_text").length) {
        init_quill("#new_comment_text");
    }
});


function menu_highlight() {
    let protocol = window.location.protocol;
    let pathname = window.location.pathname;
    let root = window.location.hostname;
    let port = window.location.port;

    let url = protocol + "//" + root;
    // to deal with custom port (Hi flask)
    if (port) { url = url + ":" + port };
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
    out = window.location.protocol + "//" + window.location.host + ROOT_PATH + path;
    return out;
}


function display_alerts() {
    let msg = window.sessionStorage.getItem("message_success");
    if (msg){
        createSuccess(msg);
        window.sessionStorage.removeItem("message_success");
    }
}


function createError(msg, title){
    toastr.options = toastrOptions;
    toastr["error"](msg, title);
}


function createSuccess(msg){
    toastr.options = toastrOptions;
    toastr["success"](msg);
}


function showError(response){
    let answer = response.responseJSON;
    if (answer == null) {
        answer = {
            'fr': {
                'message': "Une erreur inattendue s'est produite. Désolé :("
            },
            'en': {
                'message': "An unexpected error happened. Sorry :("
            }
        }
    };

    let content = answer[LANGUAGE];
    createError(content.message, content.title);
}


function showSuccess(response){
    let content = response[LANGUAGE];
    window.sessionStorage.setItem("message_success", content);
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
    if (LANGUAGE == "fr") {
        createError("Certains champs ne sont pas remplis !");
    }
    else{
        createError("Some fields are not filled in !");
    }
}

function set_date_picker() {
    if (LANGUAGE == 'fr') {
        $.datepicker.setDefaults( $.datepicker.regional[ "fr" ] );
        $('[date_picker="true"]').attr("placeholder", "jj/mm/aaaa");
    } else {
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


function init_quill(element_id) {

    let text = "Enter your comment here...";

    if (LANGUAGE == "fr") {
        text = "Saisir votre commentaire...";
    }

    if (!(element_id in QUILLS)) {
        QUILLS[element_id] = new Quill(element_id, {
            modules: {
                toolbar: [
                    [{ header: [1, 2, false]}],
                    ['bold', 'italic', 'underline', 'strike'],
                    [{color: []}],
                    ['clean'],
                ]
            },
            placeholder: text,
            theme: 'snow'  // or 'bubble'
        });
    };

    return QUILLS[element_id];
}
