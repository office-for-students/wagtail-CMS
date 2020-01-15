$(document).ready(function(){
    var btn = document.getElementById("back-btn");
    var previousPageUrl = sessionStorage.getItem('resultsPageUrl');

    if(previousPageUrl) {
        btn.href= previousPageUrl;
        btn.style.visibility = "visible";
    }
})
