(function ($) {

    var CookieBanner = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    CookieBanner.prototype = {
        setup: function() {
            this.acceptBtn = this.wrapper.find('.cookie-banner__ok');
            this.findOutMoreBtn = this.wrapper.find('.cookie-banner__find-out-more');

            this.startWatchers();
        },

        startWatchers: function() {
            var that = this;

            this.acceptBtn.click(function() {
                document.cookie = "discoverUniCookies=accepted; expires=Thu, 31 Dec 2050 23:59:59 UTC";
                that.wrapper.hide();
            });

            this.findOutMoreBtn.click(function() {
                if (location.pathname.indexOf('/cy/') === -1) {
                    location.pathname = '/cookies/';
                } else {
                    location.pathname = '/cy/cookies/';
                }
            });
        }
    }

    function init() {
        var cookieBanner = $('.cookie-banner');
        for (var i = 0; i < cookieBanner.length; i++) {
            new CookieBanner(cookieBanner[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
