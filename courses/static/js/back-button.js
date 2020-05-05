(function ($) {
    function init() {
        var form = $("#back_to_search");
        var lastSearch = JSON.parse(sessionStorage.getItem("lastSearch"));

        if(lastSearch) {
            for (var i = 0; i < lastSearch.length; i++ ) {
                var formInput = document.createElement('input');
                formInput.setAttribute('type', 'text');
                formInput.setAttribute('name', lastSearch[i].name);
                formInput.setAttribute('value', lastSearch[i].value);
                form.append(formInput);
            }

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
