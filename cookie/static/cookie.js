// COOKIE BANNER
var CookieBanner = function (wrapper) {
    this.wrapper = $(wrapper);
    this.setup();
}

CookieBanner.prototype = {
    setup: function () {
        this.acceptBtn = this.wrapper.find('.cookie-banner__ok');
        this.findOutMoreBtn = this.wrapper.find('.cookie-banner__find-out-more');
        if (localStorage.discoverUniCookies === 'accepted') {
            document.cookie = "discoverUniCookies=accepted;";
            this.wrapper.hide();
        }

        this.startWatchers();
    },

    startWatchers: function () {
        var that = this;

        this.acceptBtn.click(function () {
            document.cookie = "discoverUniCookies=accepted;";
            localStorage.discoverUniCookies = 'accepted';
            that.wrapper.hide();
        });
    }
}