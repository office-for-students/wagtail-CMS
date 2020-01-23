$(document).ready(function() {
    var btnVisibility = sessionStorage.getItem("btnVisibility");

    if(btnVisibility) {
        var btn = document.getElementById("course-detail__nav-control-back");
        btn.style.visibility = "visible";  

        $("#course-detail__nav-control-back").click(function(evt) {
            evt.preventDefault();
            history.go(-1);
            sessionStorage.removeItem('btnVisibility');
        }); 
    }
});

