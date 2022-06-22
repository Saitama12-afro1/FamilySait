function window_form(){
    var tag_visable = document.getElementById("form_task");
    tag_visable.hidden = !tag_visable.hidden    
    };


function taskDescription(task_id){
        var tag_visable = document.getElementById("task_description" + task_id);
        tag_visable.hidden = !tag_visable.hidden    
        }  