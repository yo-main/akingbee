
function submit_apiary_modal(){
    let apiary_id = $("#apiary_id").attr("name");
    let my_url = get_full_url("/api/apiary/" + apiary_id);

    let data = {
        "name": $("#apiary_name_modal").val(),
        "location": $("#apiary_location_modal").val(),
        "status": $("#apiary_status_modal").val(),
        "honey": $("#apiary_honey_modal").val(),
    }

    $.ajax({
        type: "PUT",
        url: my_url,
        data: data,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            $("#edit_apiary").modal("hide");
            showSuccess(answer);
            window.location.reload();
        }
    });
}


function modal_apiary_edit(button){
    let apiary_id = button.name.substring(5);
    let my_url = get_full_url("/api/apiary/" + apiary_id);

    $.ajax({
        type: "GET",
        url: my_url,
        error: function(answer, code){
            showError(answer);
        },
        success: function(answer, code){
            let apiary = answer;
            $("#edit_apiary").modal("show");
            
            $("#apiary_name_modal").val(apiary.name);
            $("#apiary_location_modal").val(apiary.location);
            $("#apiary_status_modal").val(apiary.status_id).change();
            $("#apiary_honey_modal").val(apiary.honey_type_id).change();

            $("#apiary_id").attr("name", apiary_id);
            $("#apiary_name_modal").attr("name", apiary.name);
            $("#apiary_location_modal").attr("name", apiary.location);
            $("#apiary_status_modal").attr("name", apiary.status);
            $("#apiary_honey_modal").attr("name", apiary.honey_type);
        }
    });
}


function delete_apiary(button){
    let apiary_id = button.name.substring(5);
    let confirm;
    let my_url = get_full_url("/api/apiary/" + apiary_id);

    if (LANGUAGE == "fr"){
        confirm = window.confirm("Supprimer ce rucher ?");
    }
    else{
        confirm = window.confirm ("Delete this apiary ?");
    }

    if (confirm){
        $.ajax({
            type: "DELETE",
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
