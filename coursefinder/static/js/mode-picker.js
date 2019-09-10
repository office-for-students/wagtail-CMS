(function ($) {

    var ModePicker = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    ModePicker.prototype = {
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
                var modes = []
                for (var i = 0; i < this.mode.length; i++) {
                  if (this.mode[i].checked) {
                    modes.push(this.mode[i].value)
                  }
                }
                sessionStorage.setItem("modes", modes);
            });
        }
    }

    function init() {
        var modePickers = $('.mode-chooser');
        new ModePicker(modePickers[0]);
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
