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
        hideSelectedCoursElement: function (el_id) {
            let course_to_remove = document.getElementById(el_id);
            course_to_remove.classList.add("hidden");
        },


        handleCourseRemoval: function (removedCourse) {
            let HTMLID = getCourseID(removedCourse);
            for (var i = 0; i < this.selectedCourses.length; i++) {
                var course = this.selectedCourses[i];
                if (this.isCourse(course, removedCourse)) {
                    this.selectedCourses.splice(i, 1);
                }
                if (this.compareCourses) {
                    for (var index = 0; index < this.compareCourses.length; index++) {
                        if (this.compareCourses[index].id == HTMLID) {
                            this.compareCourses.splice(index, 1);

                        }
                    }
                }
            }
            this.updateBookmarkNumber();
            this.hideSelectedCoursElement(HTMLID);
            localStorage.setItem('comparisonCourses', JSON.stringify(this.selectedCourses));
            localStorage.setItem('compareCourses', JSON.stringify(this.compareCourses));

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


let checked_bookmark = 0
var id_list = [];

function getSavedCourses() {
    if (!localStorage.getItem('compareCourses')) {
        return [];
    }

    return JSON.parse(localStorage.getItem('compareCourses'));
}

var compare_list = getSavedCourses();

function getComparisonCourses() {
    if (!localStorage.getItem("comparisonCourses")) {

        return [];
    }
    return JSON.parse(localStorage.getItem("comparisonCourses"));
}

function setSavedCourses(compare_list) {
    if (compare_list != null) {
        localStorage.setItem('compareCourses', JSON.stringify(compare_list));
    }
}


function compareButtonFormat(checked, id) {
    var compare_button = document.getElementById('compare-courses-button')
    var compare_text = document.getElementById('bookmark-text')
    var courses_selected = document.getElementById('courses-selected')

    if (checked) {
        checked_bookmark += 1
    } else {
        checked_bookmark -= 1
    }

    if (checked_bookmark >= 1) {
        courses_selected.innerHTML = "<strong>" + checked_bookmark + " {% get_translation key="
        courses_selected
        " language=page.get_language %}</strong>"
    } else {
        courses_selected.innerHTML = ""
    }

    if (2 <= checked_bookmark && checked_bookmark <= 7) {
        compare_button.classList.add("enabled")
        compare_button.disabled = false
        compare_text.innerHTML = "{% get_translation key='select_up_to_7' language=page.get_language %}"
        courses_selected.classList.remove("red")
    } else if (7 < checked_bookmark) {
        courses_selected.classList.add("red")
        compare_button.classList.remove("enabled")
        compare_button.disabled = true
    } else {
        compare_button.disabled = true
        compare_button.classList.remove("enabled")
        compare_text.innerHTML = "Select at least 2 courses to compare"
    }


    const compare_list = getSavedCourses();
    if (checked) {
        let course = {"id": id, "rating": 0}
        compare_list.push(course);
    } else {
        for (var i = 0; i < compare_list.length; i++) {
            if (compare_list[i].id === id) {
                let index = compare_list.indexOf(compare_list[i])
                compare_list.splice(index, 1)
            }
        }
    }
    setSavedCourses(compare_list);
}

function buttonFormat() {
    var compare_button = document.getElementById('compare-courses-button')
    var compare_text = document.getElementById('bookmark-text')
    var courses_selected = document.getElementById('courses-selected')

    if (checked_bookmark >= 1) {
        courses_selected.innerHTML = "<strong>" + checked_bookmark + " {% get_translation key='courses_selected' language=page.get_language %}</strong>"
    } else {
        courses_selected.innerHTML = ""
    }
    if (2 <= checked_bookmark && checked_bookmark <= 7) {
        compare_button.classList.add("enabled")
        compare_button.disabled = false
        compare_text.innerHTML = "{% get_translation key='select_up_to_7' language=page.get_language %}"
        courses_selected.classList.remove("red")
    } else if (7 < checked_bookmark) {
        courses_selected.classList.add("red")
        compare_button.classList.remove("enabled")
        compare_button.disabled = true
    } else {
        compare_button.disabled = true
        compare_button.classList.remove("enabled")
        compare_text.innerHTML = "{% get_translation key='select_at_least_2' language=page.get_language %}"
    }
}

function checkSelectedOnLoad(ids) {
    let compare_list = getSavedCourses();
    for (var i = 0; i < compare_list.length; i++) {
        let none = compare_list[i].id.toLowerCase().replace("-checkbox", "");
        console.log("compare list id = ", none, " id passed in = ", ids);
        if (ids.includes(none)) {
            var index = ids.indexOf(none);
            document.getElementById(ids[index] + "-checkbox").checked = true;
            checked_bookmark += 1;
        }
    }
}

function getCourseID(course) {
    let courseId = course.courseId;
    let studyMode = course.mode.en;
    let htmlID = courseId + "-" + studyMode.replace(" ", "-") + "-container";
    return htmlID.toLowerCase();
}


function savedInstitutions() {
    let saved_institutions = getComparisonCourses();
    console.log("saved_instutions ", saved_institutions)
    for (let i = 0; i < saved_institutions.length; i++) {
        let containing_div = document.getElementById("institution-bookmark");
        console.log("containing div ", containing_div);
        let course = saved_institutions[i];
        let courseHTMLID = getCourseID(course);
        id_list.push(courseHTMLID)
        let query = course.uniId + ',' + course.courseId + ',' + course.mode.en
        containing_div.innerHTML += `
            <div class="bookmark-container" id="${courseHTMLID}">
                <input id="${courseHTMLID}-checkbox" class="bookmark-check" style="margin-right: 95px; margin-bottom:auto; margin-top: 40px" name="courses"  type="checkbox"
onchange="compareButtonFormat(checked, id)" value="${query}">
                <div id='course-${i}' class='bookmark__course'>
                    <a href='' class='bookmark__course-name'></a>
                    <p class="bookmark__course-info length">
                        <span class="unknown">{% get_translation key='course_length_not_available' language=page.get_language %}</span>
                        <span class="known"><span class="length"></span>-{% get_translation key='year_course' language=page.get_language %}</span>
                    </p>
                    <p class="bookmark__course-info mode">
                        {% get_translation key='study_mode' language=page.get_language %}: <span class="mode"></span>
                    </p>

                    <p class="bookmark__course-info distance">
                        {% get_translation key='distance_learning' language=page.get_language %}: <span class="distance"></span>
                    </p>

                    <p class="bookmark__course-info sandwich">
                        {% get_translation key='work_placement_year' language=page.get_language %}: <span class="sandwich"></span>
                    </p>

                    <p class="bookmark__course-info abroad">
                        {% get_translation key='year_abroad' language=page.get_language %}: <span class="abroad"></span>
                    </p>

                    <p class="bookmark__course-info location">
                        {% get_translation key='location' language=page.get_language %}: <span class="location"></span>
                    </p>

                    <button type="button" class="bookmark__course-remove">
                        <img class="bookmark__course-remove-icon" src="{% static 'images/bin.svg' %}" alt=""> {% get_translation key='remove_course' language=page.get_language %}
                    </button>
                </div>
            </div>`
    }
    checkSelectedOnLoad(id_list);
}

savedInstitutions();
buttonFormat();

$.ajax({
    url: '/course-details/translations/',
    type: 'POST',
    contentType: 'application/json; charset=utf-8',
    processData: false,
    data: JSON.stringify({
            "terms": [
                "select_up_to_7",
                "courses_selected",
                "course_length_not_available",
                "year_course",
                "study_mode",
                "distance_learning",
                "work_placement_year",
                "year_abroad",
                "location",
                "remove_course"
            ],
            "language": "cy"
        }
    ),
});
