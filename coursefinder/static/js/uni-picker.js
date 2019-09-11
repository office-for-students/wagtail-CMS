(function ($) {

    var UniPicker = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    UniPicker.prototype = {
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
                var uni = this.uni.value
                sessionStorage.setItem("uni", uni)
            });
        }
    }

    function init() {
        var uniPickers = $('.uni-picker');
        new UniPicker(uniPickers[0]);
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
