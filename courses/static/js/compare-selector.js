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
            this.compareAdd = this.compareBar.find('.compare-popup__add');
            this.compareCount = this.compareBar.find('.compare-popup__count .count');
            this.compareNotEnough = this.compareBar.find('.compare-popup__not-enough');
            this.compareEnough = this.compareBar.find('.compare-popup__enough');
            this.compareRemove = this.compareBar.find('.compare-popup__remove');

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
            });

            this.compareClose.click(function() {
                that.compareBar.slideUp('slow');
            });
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
            this.compareAdd.hide();
            this.compareRemove.show();
            this.compareBar.slideDown("slow");
        },

        handleCourseAddition: function() {
            this.button.addClass('selected');
            this.selectedCourses.push({'uniId': this.uniId, 'courseId': this.courseId, 'mode': this.mode});
            localStorage.setItem('comparisonCourses', JSON.stringify(this.selectedCourses));
            this.courseSelected = true;
            this.compareCount.text(this.selectedCourses.length);
            if (this.selectedCourses.length < 2) {
                this.compareNotEnough.show();
                this.compareEnough.hide();
            } else {
                this.compareNotEnough.hide();
                this.compareEnough.show();
            }
            this.compareAdd.show();
            this.compareRemove.hide();
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
