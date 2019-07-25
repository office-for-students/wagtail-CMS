(function ($) {

    var AccordionGroup = function (wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    AccordionGroup.prototype = {
        setup: function() {
            this.accordions = [];
            this.activeAccordion = null;

            this.initialiseAccordions();
        },

        initialiseAccordions: function()  {
            var accordions = this.wrapper.find('.course-detail__accordion');
            for (var i = 0; i < accordions.length; i++) {
                this.accordions.push(new Accordion(accordions[i], this.handleAccordionOpen.bind(this), this.handleAccordionClose.bind(this)));
            }
        },

        setActiveAccordion: function(accordion) {
            this.activeAccordion = accordion;
        },

        handleAccordionOpen: function(accordion) {
            if (this.activeAccordion) {
                this.activeAccordion.collapse();
            }
            this.setActiveAccordion(accordion);
        },

        handleAccordionClose: function() {
            this.setActiveAccordion(null);
        }
    }

    var Accordion = function(wrapper, openCallback, closeCallback) {
        this.wrapper = $(wrapper);
        this.openCallback = openCallback;
        this.closeCallback = closeCallback;
        this.setup();
    }

    Accordion.prototype = {
        setup: function() {
            this.id = this.wrapper[0].id;
            this.header = this.wrapper.find('.course-detail__accordion-heading');
            this.body  = this.wrapper.find('.course-detail__accordion-body');
            this.plusIcon = this.wrapper.find('.plus');
            this.minusIcon = this.wrapper.find('.minus');
            this.isOpen = false;

            this.setInitialView();
            this.startWatcher();
        },

        setInitialView: function() {
            this.body.hide();
            this.plusIcon.show();
        },

        startWatcher: function() {
            var that = this;
            this.header.click(this.handleClick.bind(this))
        },

        handleClick: function() {
            if (this.isOpen) {
                this.collapse();
            } else {
                this.open();
            }
        },

        open: function() {
            this.isOpen = !this.isOpen;
            this.plusIcon.hide();
            this.minusIcon.show();
            this.body.show();
        },

        collapse: function() {
            this.isOpen = !this.isOpen;
            this.plusIcon.show();
            this.minusIcon.hide();
            this.body.hide();
        }
    }

    function init() {
        var accordionGroups = $('.course-detail__accordion-block');
        for (var i = 0; i < accordionGroups.length; i++) {
            new AccordionGroup(accordionGroups[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
