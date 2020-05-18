(function ($) {

    var InstitutionExplanationGroup = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    InstitutionExplanationGroup.prototype = {
        setup: function() {
            this.link = this.wrapper.find('.explanation__link');
            this.linkText = this.link.find('.information-link');
            this.popup = new InstitutionExplanationPopUp(this.wrapper.find('.institution-explanation'),
                                                            this.returnFocus.bind(this));

            this.startWatcher();
        },

        startWatcher: function() {
            var that = this;
            this.link.click(function() {
                that.popup.show();
            })
        },

        returnFocus: function() {
            this.linkText.focus()
        }
    }

    InstitutionExplanationPopUp = function(popup, returnFocus){
        this.popup = popup;
        this.returnFocus = returnFocus;
        this.setup();
    }

    InstitutionExplanationPopUp.prototype = {
        setup: function() {
            this.isOpen = false;
            this.closeBtn = this.popup.find('.institution-explanation__close');

            this.startWatcher();
        },

        startWatcher: function() {
            var that = this;
            this.closeBtn.click(function() {
                that.hide();
            });

            document.addEventListener("focus", function(evt) {
                if (that.isOpen && !that.popup[0].contains(evt.target)) {
                    event.stopPropagation();
                    that.popup.focus();
                }
            }, true);

            document.addEventListener("keydown", function(evt) {
                if (that.isOpen && evt.keyCode == 27) {
                    that.popup.hide();
                }
            }, true);
        },

        show: function() {
            this.isOpen = true;
            this.popup.show();
            this.focus();
        },

        hide: function() {
            this.isOpen = false;
            this.popup.hide();
            this.returnFocus();
        },

        focus: function() {
            this.popup.focus();
        }
    }

    function init() {
        var explanationBlocks = $('.explanation');
        for (var i = 0; i < explanationBlocks.length; i++) {
            new InstitutionExplanationGroup(explanationBlocks[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
