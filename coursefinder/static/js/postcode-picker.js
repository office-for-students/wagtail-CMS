(function ($) {

    var PostcodePicker = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    PostcodePicker.prototype = {
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
                var postcode = this.postcode.value.replace(' ', '');
                var distance = this.distance.value ? this.distance.value : 10;
                if (postcode) {
                    var queryValue = [postcode,  distance].join(',');

                    sessionStorage.setItem("postcode", queryValue);
                }
            });
        }
    }

    function init() {
        var postcodePickers = $('.postcode-search');
        new PostcodePicker(postcodePickers[0]);
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
