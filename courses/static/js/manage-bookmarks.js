(function ($) {

    var BookmarkPage = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    BookmarkPage.prototype = {
        setup: function() {
            this.isEnglish = location.pathname.indexOf('/cy/') === -1;
            this.courseCountSpan = this.wrapper.find('.count');
            this.navBox = this.wrapper.find('.bookmark__nav-box');
            this.noneSelected = this.wrapper.find('.bookmark__none-selected');
            this.oneSelected = this.wrapper.find('.bookmark__one-selected');
            this.courseBoxes = this.wrapper.find('.bookmark__course');
            this.selectedCourses = [];

            this.loadSelectedCourses();
            this.setInitialView();
        },

        loadSelectedCourses: function() {
            if (JSON.parse(localStorage.getItem('comparisonCourses'))) {
                this.selectedCourses = JSON.parse(localStorage.getItem('comparisonCourses'));
            } else {
                this.selectedCourses = [];
            }
        },

        setInitialView: function() {
            this.courseCountSpan.text(this.selectedCourses.length);

            if (this.selectedCourses.length === 0) {
                this.navBox.hide();
                this.noneSelected.show();
            }

            if (this.selectedCourses.length === 1) {
                this.navBox.hide();
                this.oneSelected.show();
            }

            this.courseBlocks = [];
            for (var i = 0; i < this.selectedCourses.length; i++) {
                this.courseBlocks.push(new CourseBlock(this.courseBoxes[i], this.selectedCourses[i], this.isEnglish,
                                                        this.handleCourseRemoval.bind(this)));
            }
        },

        handleCourseRemoval: function(removedCourse) {
            for (var i = 0; i < this.selectedCourses.length; i++) {
                var course = this.selectedCourses[i];
                if (this.isCourse(course, removedCourse)) {
                    this.selectedCourses.splice(i, 1);
                }
            }
            localStorage.setItem('comparisonCourses', JSON.stringify(this.selectedCourses));
            location.reload();
        },

        isCourse: function(course, removedCourse) {
            return course.uniId === removedCourse.uniId && course.courseId === removedCourse.courseId && course.mode === removedCourse.mode;
        }
    }

    var CourseBlock = function(wrapper, course,  isEnglish, handleCourseRemoval) {
        this.wrapper = $(wrapper);
        this.course = course;
        this.isEnglish = isEnglish;
        this.handleCourseRemoval = handleCourseRemoval;
        this.setup();
    }

    CourseBlock.prototype = {
        setup: function() {
            console.log('initialising course',  this.course);
            this.courseNameSpan = this.wrapper.find('.bookmark__course-name');
            this.lengthBlock = this.wrapper.find('.bookmark__course-info.length');
            this.lengthUnknown = this.lengthBlock.find('.unknown');
            this.lengthKnown = this.lengthBlock.find('.known');
            this.courseLengthSpan = this.lengthBlock.find('.length');
            this.courseModeSpan = this.wrapper.find('.bookmark__course-info.mode .mode');
            this.courseDistanceSpan = this.wrapper.find('.bookmark__course-info.distance .distance');
            this.courseSandwichSpan = this.wrapper.find('.bookmark__course-info.sandwich .sandwich');
            this.courseAbroadSpan = this.wrapper.find('.bookmark__course-info.abroad .abroad');
            this.courseLocationSpan = this.wrapper.find('.bookmark__course-info.location .location');
            this.removeBtn = this.wrapper.find('.bookmark__course-remove');

            this.setInitialView();
            this.startWatcher();
        },

        setInitialView: function() {
            this.courseNameSpan.text(this.course.courseName);
            this.courseLengthSpan.text(this.course.length);
            this.courseModeSpan.text(this.course.mode);
            this.courseDistanceSpan.text(this.course.distance);
            this.courseSandwichSpan.text(this.course.sandwich);
            this.courseAbroadSpan.text(this.course.abroad);
            this.courseLocationSpan.text(this.course.locations);

            if (this.isEnglish) {
                this.courseNameSpan.attr('href', '/course-details/' + this.course.uniId + '/' + this.course.courseId + '/' + this.course.mode + '/');
            } else {
                this.courseNameSpan.attr('href', '/cy/course-details/' + this.course.uniId + '/' + this.course.courseId + '/' + this.course.mode + '/');
            }
            if (this.course.length === '' || this.course === 'None') {
                this.lengthKnown.hide();
            } else {
                this.lengthUnknown.hide();
            }

            this.wrapper.show();
        },

        startWatcher: function() {
            var that = this;

            this.removeBtn.click(function() {
                that.handleCourseRemoval(that.course)
            });
        }
    }

    function init() {
        var bookmarkWrapper = $('.bookmark');
        for (var i = 0; i < bookmarkWrapper.length; i++) {
            new BookmarkPage(bookmarkWrapper[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
