(function ($) {

    var BookmarkPage = function (wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    BookmarkPage.prototype = {
        setup: function () {
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

        loadSelectedCourses: function () {
            if (JSON.parse(localStorage.getItem('comparisonCourses'))) {
                this.selectedCourses = JSON.parse(localStorage.getItem('comparisonCourses'));
                this.compareCourses = JSON.parse(localStorage.getItem('compareCourses'));
            } else {
                this.selectedCourses = [];
                this.compareCourses = [];
            }
        },

        setInitialView: function () {
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
        updateBookmarkNumber: function () {
            let bookmark_el = document.getElementsByClassName('nav-bookmark__count')[0]
            let total_bookmark = parseInt(bookmark_el.innerHTML);
            total_bookmark = total_bookmark - 1;
            if (total_bookmark === 0) {
                bookmark_el.classList.add("hidden");
            } else {
                bookmark_el.innerHTML = total_bookmark.toString();
            }
        },

        handleCourseRemoval: function (removedCourse) {
            for (var i = 0; i < this.selectedCourses.length; i++) {
                var course = this.selectedCourses[i];
                if (this.isCourse(course, removedCourse)) {
                    this.selectedCourses.splice(i, 1);
                }
                if (this.compareCourses) {
                    for (var index = 0; index < this.compareCourses.length; index++) {
                        if (this.compareCourses[index].id == removedCourse.courseId) {
                            this.compareCourses.splice(index, 1);

                        }
                    }
                }
            }
            this.updateBookmarkNumber();
            localStorage.setItem('comparisonCourses', JSON.stringify(this.selectedCourses));
            localStorage.setItem('compareCourses', JSON.stringify(this.compareCourses));
            let course_to_remove = document.getElementById("" + removedCourse.courseId + "-container");
            course_to_remove.classList.add("hidden");
        },

        isCourse: function (course, removedCourse) {
            return course.uniId === removedCourse.uniId && course.courseId === removedCourse.courseId && course.mode === removedCourse.mode;
        }
    }

    var CourseBlock = function (wrapper, course, isEnglish, handleCourseRemoval) {
        this.wrapper = $(wrapper);
        this.course = course;
        this.isEnglish = isEnglish;
        this.handleCourseRemoval = handleCourseRemoval;
        this.setup();
    }

    CourseBlock.prototype = {
        setup: function () {
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

        setInitialView: function () {
            this.courseNameSpan.text(this.course.courseName + ' - ' + this.course.uniName);
            this.courseLengthSpan.text(this.course.length);
            this.courseLocationSpan.text(this.course.locations);
            if (this.isEnglish) {
                this.courseModeSpan.text(this.course.mode.en);
                this.courseDistanceSpan.text(this.course.distance.en);
                this.courseSandwichSpan.text(this.course.sandwich.en);
                this.courseAbroadSpan.text(this.course.abroad.en);
            } else {
                this.courseModeSpan.text(this.course.mode.cy);
                this.courseDistanceSpan.text(this.course.distance.cy);
                this.courseSandwichSpan.text(this.course.sandwich.cy);
                this.courseAbroadSpan.text(this.course.abroad.cy);
            }

            var mode = 'FullTime';

            if (this.course.mode.en === 'Full time') {
                mode = 'FullTime';
            } else if (this.course.mode.en === 'Part time') {
                mode = 'PartTime';
            }

            if (this.isEnglish) {
                this.courseNameSpan.attr('href', '/course-details/' + this.course.uniId + '/' + this.course.courseId + '/' + mode + '/');
            } else {
                this.courseNameSpan.attr('href', '/cy/course-details/' + this.course.uniId + '/' + this.course.courseId + '/' + mode + '/');
            }

            if (this.course.length === '' || this.course.length === 'None' || this.course === 'None') {
                this.lengthKnown.hide();
            } else {
                this.lengthUnknown.hide();
            }

            this.wrapper.show();
        },

        startWatcher: function () {
            var that = this;

            this.removeBtn.click(function () {
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
