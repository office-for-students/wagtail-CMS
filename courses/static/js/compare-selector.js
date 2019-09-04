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
                if (this.isCourse(course)) {
                    this.courseSelected = true;
                }
            }
        },

        isCourse: function(course) {
            return course.uniId === this.uniId && course.courseId === this.courseId && course.mode === this.mode;
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
                    that.button.removeClass('selected');
                    for (var i = 0; i < that.selectedCourses.length; i++) {
                        var course = that.selectedCourses[i];
                        if (that.isCourse(course)) {
                            that.selectedCourses.splice(i, 1);
                        }
                    }
                    localStorage.setItem('comparisonCourses', JSON.stringify(that.selectedCourses));
                    that.courseSelected = false;
                } else {
                    that.button.addClass('selected');
                    that.selectedCourses.push({'uniId': that.uniId, 'courseId': that.courseId, 'mode': that.mode});
                    localStorage.setItem('comparisonCourses', JSON.stringify(that.selectedCourses));
                    that.courseSelected = true;
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
