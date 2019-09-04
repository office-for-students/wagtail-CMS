(function ($) {

    var CompareSelector = function(button) {
        this.button = $(button);
        this.setup();
    }

    CompareSelector.prototype = {
        setup: function() {
            this.courseSelected = false;

            var url = location.pathname.split('/');
            if (url[1] === 'cy') {
                this.uniId = url[3];
                this.courseId = url[4];
                this.mode = url[5];
            } else {
                this.uniId = url[2];
                this.courseId = url[3];
                this.mode = url[4];
            }

            this.loadSelectedCourses();
            this.setInitialView();
            this.startWatcher();
        },

        loadSelectedCourses: function() {
            if (JSON.parse(localStorage.getItem('comparisonCourses'))) {
                this.selectedCourses = JSON.parse(localStorage.getItem('comparisonCourses'));
            } else {
                this.selectedCourses = [];
            }
            this.setCourseSelected();
        },

        setCourseSelected: function() {
            for (var i = 0; i < this.selectedCourses.length; i++) {
                var course = this.selectedCourses[i];
                if (course.uniId === this.uniId && course.courseId === this.courseId && course.mode === this.mode) {
                    this.courseSelected = true;
                }
            }
        },

        setInitialView: function() {
            if (this.courseSelected) {
                this.button.addClass('selected');
            }
        },

        startWatcher: function() {
            var that = this;
            this.button.click(function() {
                if (that.button.hasClass('selected')) {
                    console.log('removing from basket');
                    that.button.removeClass('selected');
                } else {
                    console.log('adding to basket');
                    that.button.addClass('selected');
                }
            })
        }
    }

    function init() {
        var compareBtns = $('.course-detail__compare-btn');
        for (var i = 0; i < compareBtns.length; i++) {
            new CompareSelector(compareBtns[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
