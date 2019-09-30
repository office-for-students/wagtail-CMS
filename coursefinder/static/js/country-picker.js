(function ($) {

    var CountryPicker = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    CountryPicker.prototype = {
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
                var countries = [];
                for (var i = 0; i < this.country.length; i++) {
                    if (this.country[i].checked) {
                        countries.push(this.country[i].value)
                    }
                }
                sessionStorage.setItem("countries", countries);
            })
        }
    }

    function init() {
        var countryPickers = $('.country-chooser');
        new CountryPicker(countryPickers[0]);
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
