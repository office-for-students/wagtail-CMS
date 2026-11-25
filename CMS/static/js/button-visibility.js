$(document).ready(function(){
    $(".course-finder-results__result-accordion-body-course-name").click(function() {
        sessionStorage.setItem('btnVisibility', true);
        var btnVisibility = sessionStorage.getItem("btnVisibility");
    });
    $(".bookmark__course-name").click(function() {
        sessionStorage.setItem('btnVisibility', true);
        var btnVisibility = sessionStorage.getItem("btnVisibility");
    });
});