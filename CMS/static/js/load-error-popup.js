(function ($) {

    var LoadErrorPopup = function(loadErrorBar) {
        this.loadErrorBar = $(loadErrorBar);
        this.setup();
    }

    LoadErrorPopup.prototype = {
        setup: function() {

            this.loadErrorClose = this.loadErrorBar.find('.load-error-popup__close');
            this.loadErrorNotFound = this.loadErrorBar.find('.load-error-popup__not-found');
            this.loadErrorInternalError = this.loadErrorBar.find('.load-error-popup__internal-error');
            this.loadErrorCode = this.loadErrorBar.data('error')

            this.setInitialView();
            this.startWatcher();
        },

        setInitialView: function() {
            if (this.loadErrorCode == 0) {
                this.loadErrorNotFound.show()
                this.loadErrorInternalError.hide()
            }

            if (this.loadErrorCode == 1) {
                this.loadErrorNotFound.hide()
                this.loadErrorInternalError.show()
            }
        },

        startWatcher: function() {
            var that = this;

            this.loadErrorClose.click(function() {
                that.loadErrorBar.slideUp('slow');
            });
        }
    }

    function init() {
        var loadErrorBars = $('.load-error-popup');

        if (loadErrorBars.length > 0)
            new LoadErrorPopup(loadErrorBars[0]);
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))