(function ($) {

    var CompareSelector = function(wrapper, compareBar) {
        this.wrapper = $(wrapper);
        this.compareBar = $(compareBar);
        this.setup();
    }

    CompareSelector.prototype = {
        setup: function() {
            this.navBar = $('.discover-uni-nav');
            this.button = this.wrapper.find('[class$=compare-btn]');
            this.courseSelected = false;
            this.courseName = this.wrapper.data().coursename;
            this.uniName = this.wrapper.data().uniname;
            this.uniId = this.wrapper.data().uniid;
            this.courseId = this.wrapper.data().courseid;
            this.mode = this.wrapper.data().mode;
            this.length = this.wrapper.data().length;
            this.distance = this.wrapper.data().distance;
            this.sandwich = this.wrapper.data().sandwich;
            this.abroad = this.wrapper.data().abroad;
            this.locations = this.wrapper.data().locations;

            this.compareClose = this.compareBar.find('.compare-popup__close');
            this.compareAdd = this.compareBar.find('.compare-popup__add');
            this.compareCount = this.compareBar.find('.compare-popup__count .count');
            this.compareNotEnough = this.compareBar.find('.compare-popup__not-enough');
            this.compareEnough = this.compareBar.find('.compare-popup__enough');
            this.compareRemove = this.compareBar.find('.compare-popup__remove');
            this.compareTooMany = this.compareBar.find('.compare-popup__too-many');

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
            this.navBar.trigger('loadeddata');
            this.courseSelected = false;
            this.compareAdd.hide();
            this.compareRemove.show();
            this.compareTooMany.hide();
            this.compareBar.slideDown("slow");
        },

        handleCourseAddition: function() {
            if (this.selectedCourses.length === 10) {
                this.compareAdd.hide();
                this.compareRemove.hide();
                this.compareTooMany.show();
            } else {
                this.button.addClass('selected');
                this.selectedCourses.push({'uniId': this.uniId, 'courseId': this.courseId, 'mode': this.mode,
                                            'courseName': this.courseName, 'uniName': this.uniName,
                                            'length': this.length, 'distance': this.distance, 'sandwich': this.sandwich,
                                            'abroad': this.abroad, 'locations': this.locations});
                localStorage.setItem('comparisonCourses', JSON.stringify(this.selectedCourses));
                this.navBar.trigger('loadeddata');
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
                this.compareTooMany.hide();
            }
            this.compareBar.slideDown("slow");
        }
    }

    function init() {
        var compareBtns = $('.comparison-course-area');
        var compareBars = $('.compare-popup');
        for (var i = 0; i < compareBtns.length; i++) {
            new CompareSelector(compareBtns[i], compareBars[0]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
