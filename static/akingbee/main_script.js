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

    if (pathname == "/beehouse/index"){
        filter_table_beehouse();
    }
    else if (pathname == "/apiary/index"){
        filter_table_apiary();
    }
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
    let language = $('html').attr("lang");
    let content = answer[language];
    let code = answer.code;
    createError(content.message, content.title);
}


function showSuccess(response){
    let language = $('html').attr("lang");
    let content = response[language];
    let code = response.code;
    window.sessionStorage.setItem("msgSuccessBody", content.message);
    window.sessionStorage.setItem("msgSuccessTitle", content.title);
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
    $("#beehouse_birthday").val(new Date().toDateInputValue());
}


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


$(document).ready(function() {
    set_active_language();
    menu_highlight();
    menu_filter();
    display_alerts();
    set_date_picker();
});


