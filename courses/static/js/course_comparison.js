(function ($) {

    var ComparePage = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    ComparePage.prototype = {
        setup: function() {
            this.courseCountSpan = this.wrapper.find('.count');
            this.course1 = $.urlParam('course1');
            this.course2 = $.urlParam('course2');
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

            this.initialiseDropdowns();
        },

        setInitialView: function() {
            this.courseCountSpan.text(this.selectedCourses.length);
        },

        initialiseDropdowns: function() {
            this.dropdown1 = new CourseDropdown(this.wrapper.find('#course1'), this.selectedCourses,
                                                this.course2, this.handleCourseSelection.bind(this));
            this.dropdown2 = new CourseDropdown(this.wrapper.find('#course2'), this.selectedCourses,
                                                this.course1, this.handleCourseSelection.bind(this));
        },

        handleCourseSelection: function(selectorId, selection) {
            if (selectorId === 'course1') {
                this.course1 = selection;
                var queryString = '?course1=' + this.course1;
                if (this.course2) {
                    queryString += '&course2=' + this.course2;
                }
                location.search = queryString;
            } else {
                this.course2 = selection;
                var queryString = '?course2=' + this.course2;
                if (this.course1) {
                    queryString += '&course1=' + this.course1;
                }
                location.search = queryString;
            }
        }
    }

    var CourseDropdown = function(wrapper, courses, otherCourse, selectionCallback) {
        this.wrapper = $(wrapper);
        this.courses = courses;
        this.otherCourse = otherCourse;
        this.selectionCallback = selectionCallback;
        this.setup();
    }

    CourseDropdown.prototype = {
        setup: function() {
            this.id = this.wrapper[0].id;
            this.selector = this.wrapper.find('select');
            this.itemsList = this.wrapper.find('.select-items');
            this.initialiseOptions();
            this.startWatcher();
        },

        initialiseOptions: function() {
            for (var i = 0; i < this.courses.length; i++) {
                var course = this.courses[i];
                if (this.otherCourse && this.otherCourse === `${course.uniId},${course.courseId},${course.mode}`) {
                    console.log(10)
                    this.selector.append(`<option value='${course.uniId},${course.courseId},${course.mode}' disabled>${course.courseName} - ${course.uniName}</option>`)
                } else {
                    console.log(20)
                    this.selector.append(`<option value='${course.uniId},${course.courseId},${course.mode}'>${course.courseName} - ${course.uniName}</option>`)
                }
            }
            this.selector.trigger('loadeddata');
            this.options = this.selector.find('option');
        },

        startWatcher: function() {
            var that = this;
            this.selector.change(function() {
                that.selectionCallback(that.id, that.selector.val());
            });
        }
    }

    function init() {
        var compareWrapper = $('.comparison');
        for (var i = 0; i < compareWrapper.length; i++) {
            new ComparePage(compareWrapper[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
