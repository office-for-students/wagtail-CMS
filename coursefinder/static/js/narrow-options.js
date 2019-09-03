(function ($) {

    var NarrowOptions = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    NarrowOptions.prototype = {
        setup: function() {
            this.form = this.wrapper.find('form');
            this.button = this.wrapper.find('.course-finder-content__next-button');
            this.error= this.wrapper.find('.course-finder-base__validation-error');
            this.inputs = this.wrapper.find('input[name=radioGroup]');

            this.startWatchers();
        },

        startWatchers: function() {
            var that = this;
            this.button.click(function(evt) {
                evt.preventDefault();
                if (that.isValidInput()) {
                    that.form.submit();
                } else {
                    that.showError();
                }
            });
        },

        isValidInput: function() {
            var selectedCount = 0;
            for (var i = 0; i < this.inputs.length; i++) {
                if (this.inputs[i].checked) {
                    selectedCount++
                }
            }
            return selectedCount === 1;
        },

        showError: function() {
            this.error.show();
        }
    }

    function init() {
        var narrowOptions = $('.narrow-search');
        new NarrowOptions(narrowOptions[0]);
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
