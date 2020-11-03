(function ($) {
    function init() {
        var form = $("#back_to_search");

        backBtn.click(function(evt) {
            window.history.back();
        });

    }

    $(document).on('page:load', init);
    $(init);
}(jQuery))
