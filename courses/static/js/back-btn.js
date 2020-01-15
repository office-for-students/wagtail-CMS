$(window).on("load",function(){
    var btn = document.getElementById("back-btn");
    var previousPageUrl = sessionStorage.getItem('resultsPageUrl');
    btn.style.visibility = "hidden";

    if(previousPageUrl) {
        btn.href= previousPageUrl;
        btn.style.visibility = "visible";
    }
},
    {once: true}
)
