(function ($) {

    var ResultsPage = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    ResultsPage.prototype = {
        setup: function() {
            this.btn = this.wrapper.find('.start-again');

            this.startWatchers();
        },

        startWatchers: function() {
            var that = this;

            this.btn.click(function() {
                sessionStorage.clear();
            });
        }
    }

    function init() {
        var resultsPages = $('.course-finder-results');
        new ResultsPage(resultsPages[0]);
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
