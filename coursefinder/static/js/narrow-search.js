(function ($) {

    var NarrowSearch = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    NarrowSearch.prototype = {
        setup: function() {
            this.btn = this.wrapper.find('.course-finder-content__next-button');
            this.form = this.wrapper.find('.course-finder-content__question-form');
            sessionStorage.setItem('uni', '')
            sessionStorage.getItem('postcode', '')

            this.startWatchers();
        },

        startWatchers: function() {
            var that = this;

            this.btn.click(function() {
                that.form.submit();
            });

            this.form.submit(function() {
                var subject_query = sessionStorage.getItem('subjectCodes')
                var mode_query = sessionStorage.getItem('modes')
                var countries_query = sessionStorage.getItem('countries')

                $("input[name='subject_query']").val(subject_query)
                $("input[name='mode_query']").val(mode_query)
                $("input[name='countries_query']").val(countries_query)
            });
        }
    }

    function init() {
        var narrowSearch = $('.narrow-search');
        new NarrowSearch(narrowSearch[0]);
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
