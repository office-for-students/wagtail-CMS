(function ($) {

    var HomePage = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    HomePage.prototype = {
        setup: function() {
            this.courseCountSpan = this.wrapper.find('.count');
            this.selectedCourses = [];

            this.loadSelectedCourses();
            this.setInitialView();
        },

        loadSelectedCourses: function() {
            if (JSON.parse(localStorage.getItem('bookmarkedCourses'))) {
                this.selectedCourses = JSON.parse(localStorage.getItem('bookmarkedCourses'));
            } else {
                this.selectedCourses = [];
            }
        },

        setInitialView: function() {
            this.courseCountSpan.text(this.selectedCourses.length);
        },

    }
   
    function init() {
        var bookmarkWrapper = $('.home-page__bookmark-body');
        new HomePage(bookmarkWrapper[0]);
        
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))