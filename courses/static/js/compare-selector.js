(function ($) {

    var CompareSelector = function(button, compareBar) {
        this.button = $(button);
        this.compareBar = $(compareBar);
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

            this.compareClose = this.compareBar.find('.compare-popup__close');
            this.compareContent = this.compareBar.find('.content');
            this.compareCount = this.compareBar.find('.compare-popup__count .count');
            this.compareNotEnough = this.compareBar.find('.compare-popup__not-enough');
            this.compareEnough = this.compareBar.find('.compare-popup__enough');

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
            this.compareBar.slideUp('slow');
        },

        startWatcher: function() {
            var that = this;
            this.button.click(function() {
                that.loadSelectedCourses();
                that.compareBar.slideUp("slow");
                if (that.button.hasClass('selected')) {
                    that.handleCourseRemoval();
                } else {
                    that.handleCourseAddition();
                }
            })
        },

        handleCourseRemoval: function() {
            this.button.removeClass('selected');
            for (var i = 0; i < this.selectedCourses.length; i++) {
                var course = this.selectedCourses[i];
                if (this.isCourse(course)) {
                    this.selectedCourses.splice(i, 1);
                }
            }
            localStorage.setItem('comparisonCourses', JSON.stringify(this.selectedCourses));
            this.courseSelected = false;
        },

        handleCourseAddition: function() {
            this.button.addClass('selected');
            this.selectedCourses.push({'uniId': this.uniId, 'courseId': this.courseId, 'mode': this.mode});
            localStorage.setItem('comparisonCourses', JSON.stringify(this.selectedCourses));
            this.courseSelected = true;
            this.compareCount.text(this.selectedCourses.length);
            if (this.selectedCourses.length < 2) {
                this.compareContent.addClass('full-width');
                this.compareNotEnough.show();
                this.compareEnough.hide();
            } else {
                this.compareContent.removeClass('full-width');
                this.compareNotEnough.hide();
                this.compareEnough.show();
            }
            this.compareContent
            this.compareBar.slideDown("slow");
        }
    }

    function init() {
        var compareBtns = $('.course-detail__compare-btn');
        var compareBars = $('.compare-popup');
        for (var i = 0; i < compareBtns.length; i++) {
            new CompareSelector(compareBtns[i], compareBars[0]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
