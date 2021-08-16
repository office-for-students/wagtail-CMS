(function ($) {
    var NavBookMarkBtn = function(btn) {
        this.btn = $(btn);
        this.setup();
    }

    NavBookMarkBtn.prototype = {
        setup: function() {
            this.navBar = $('.nav');
            this.loadSelectedCourses();
            this.startWatcher();
        },

        loadSelectedCourses: function() {
            if (JSON.parse(localStorage.getItem('bookmarkedCourses'))) {
                this.selectedCourses = JSON.parse(localStorage.getItem('bookmarkedCourses'));
            } else {
                this.selectedCourses = [];
            }
            this.btn.text(this.selectedCourses.length);
        },

        startWatcher: function() {
            var that = this;
            this.navBar.on('loadeddata', function() {
                that.loadSelectedCourses();
            })
        }
    }

    function init() {
        var bookmarkBtns = $('.nav-bookmark__count');
        for (var i = 0; i < bookmarkBtns.length; i++) {
            new NavBookMarkBtn(bookmarkBtns[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
