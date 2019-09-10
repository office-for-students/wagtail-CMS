(function ($) {

    var SubjectPicker = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    SubjectPicker.prototype = {
        setup: function() {
            this.btn = this.wrapper.find('.course-finder-content__next-button');
            this.form = this.wrapper.find('.course-finder-content__question-form');

            this.startWatchers();
        },

        startWatchers: function() {
            var that = this;

            this.btn.click(function() {
                that.form.submit();
            });

            this.form.submit(function() {
                var subject_query = sessionStorage.getItem('subjectCodes')
                var institution_query = sessionStorage.getItem('uni')
                var mode_query = sessionStorage.getItem('modes')
                var countries_query = sessionStorage.getItem('countries')
                var postcode_query = sessionStorage.getItem('postcode')

                $("input[name='subject_query']").val(subject_query)
                $("input[name='institution_query']").val(institution_query)
                $("input[name='mode_query']").val(mode_query)
                $("input[name='countries_query']").val(countries_query)
                $("input[name='postcode_query']").val(postcode_query)
            });
        }
    }

    function init() {
        var subjectPickers = $('.narrow-search');
        new SubjectPicker(subjectPickers[0]);
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
