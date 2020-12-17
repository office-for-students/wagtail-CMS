$(document).ready(function() {
    var btnVisibility = sessionStorage.getItem("btnVisibility");
    
    if(btnVisibility) {
        var btn = document.getElementById("course-detail__nav-control-back").style.visibility = "visible";  
        $("#course-detail__nav-control-back").click(function(evt) {  
            sessionStorage.removeItem('btnVisibility');
            window.history.back();
        }); 
    }
});