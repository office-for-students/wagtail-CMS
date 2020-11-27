(function ($) {
    function init() {
        var backBtn = $("#course-detail__nav-control-back");
        backBtn.click(function(evt) {
            window.history.back();
        });
    }
    $(document).on('page:load', init);
    $(init);
}(jQuery))
