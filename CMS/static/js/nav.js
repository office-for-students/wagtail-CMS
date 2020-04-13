(function ($) {

    var NavBar = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    NavBar.prototype = {
        setup: function() {
            this.mobileBurgerButton = this.wrapper.find('#burger-menu');
            this.mobileCloseButton = this.wrapper.find('#close-menu');
            this.mobileMenuBody = this.wrapper.find('.discover-uni-nav__mobile-links');
            this.startWatchers();
        },

        startWatchers: function() {
            var that = this;
            this.mobileBurgerButton.click(function() {
                that.mobileMenuBody.show();
                that.mobileBurgerButton.hide();
                that.mobileCloseButton.show();
            });

            this.mobileCloseButton.click(function() {
                that.mobileMenuBody.hide();
                that.mobileCloseButton.hide();
                that.mobileBurgerButton.show();
            });
        }
    }

    function init() {
        var navBar = $('.discover-uni-nav');
        for (var i = 0; i < navBar.length; i++) {
            new NavBar(navBar[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
