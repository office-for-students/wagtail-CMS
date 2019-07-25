(function ($) {

    var LabelExplanationGroup = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    LabelExplanationGroup.prototype = {
        setup: function() {
            this.link = this.wrapper.find('.chart-explanation__link');
            this.popup = new LabelExplanationPopUp(this.wrapper.find('.chart-label-explanation'));

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

    LabelExplanationPopUp = function(popup){
        this.popup = popup;
        this.setup();
    }

    LabelExplanationPopUp.prototype = {
        setup: function() {
            this.closeBtn = this.popup.find('.chart-label-explanation__close');

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
        var explanationBlocks = $('.chart-explanation');
        for (var i = 0; i < explanationBlocks.length; i++) {
            new LabelExplanationGroup(explanationBlocks[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
