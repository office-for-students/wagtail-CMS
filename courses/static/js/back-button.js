(function ($) {
    function init() {
        var form = $("#back_to_search");
        var courseQuery = form.find("#course_query");
        var institutionQuery = form.find("#institution_query");
        var lastSearch = JSON.parse(sessionStorage.getItem("lastSearch"));

        if(lastSearch) {
            courseQuery.val(lastSearch.course_query);
            console.log(courseQuery.val());
            institutionQuery.val(lastSearch.institution_query);

            var backBtn = $("#course-detail__nav-control-back");
            backBtn.css("visibility", "visible");

            backBtn.click(function(evt) {
                evt.preventDefault();
                
                form.submit();
            });
        }
    }

    $(document).on('page:load', init);
    $(init);
}(jQuery))
