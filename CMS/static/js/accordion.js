(function ($) {

    var Accordion = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    Accordion.prototype = {
        setup: function() {
            this.header = this.wrapper.find('[class$=accordion-header]');
            this.body  = this.wrapper.find('[class$=accordion-body]');
            this.plusIcon = this.wrapper.find('.plus');
            this.minusIcon = this.wrapper.find('.minus');

            this.setInitialView()
            this.startWatchers();
        },

        setInitialView: function() {
            this.body.hide();
            this.plusIcon.show();
        },

        startWatchers: function() {
            var that = this;
            this.header.click(this.handleAccordionToggle.bind(this));

            this.header.keydown(function(evt) {
                if(evt.which === 13 || evt.which === 32) {
                  that.handleAccordionToggle();
                }
            });
        },

        handleAccordionToggle: function() {
            if (this.header.hasClass('open')) {
                this.body.hide();
                this.plusIcon.show();
                this.minusIcon.hide();
                this.header.removeClass('open');
            }
            else {
                this.body.show();
                this.plusIcon.hide();
                this.minusIcon.show();
                this.header.addClass('open');
            }
        }
    }

    function init() {
        var accordions = $('[class$=accordion]');
        for (var i = 0; i < accordions.length; i++) {
            new Accordion(accordions[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
