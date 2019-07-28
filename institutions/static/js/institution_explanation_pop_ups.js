(function ($) {

    var InstitutionExplanationGroup = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    InstitutionExplanationGroup.prototype = {
        setup: function() {
            this.link = this.wrapper.find('.explanation__link');
            this.popup = new InstitutionExplanationPopUp(this.wrapper.find('.institution-explanation'));

            this.setInitialView();
            this.startWatcher();
        },

        setInitialView: function()  {
            this.popup.hide();
        },

        startWatcher: function() {
            var that = this;
            this.link.click(function() {
                that.popup.show();
            })
        }
    }

    InstitutionExplanationPopUp = function(popup){
        this.popup = popup;
        this.setup();
    }

    InstitutionExplanationPopUp.prototype = {
        setup: function() {
            this.closeBtn = this.popup.find('.institution-explanation__close');

            this.startWatcher();
        },

        startWatcher: function() {
            var that = this;
            this.closeBtn.click(function() {
                that.popup.hide();
            })
        },

        show: function() {
            this.popup.show();
        },

        hide: function() {
            this.popup.hide();
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
