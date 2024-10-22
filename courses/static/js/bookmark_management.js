const terms_on_page = [
    "select_up_to_7",
    "select_at_least_2",
    "courses_selected",
    "course_length_not_available",
    "year_course",
    "study_mode",
    "distance_learning",
    "work_placement_year",
    "year_abroad",
    "location",
    "remove_course",
];

let _translationTerms = {}

function fetchHTMLTerms(terms, callback) {
    $.ajax({
        url: '/course-details/translations/',
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        processData: false,
        data: JSON.stringify({
                "terms": terms_on_page,
                "language": document.documentElement.lang
            }
        ),
        success: callback
    });
}

function allTerms(callback) {
    fetchHTMLTerms(terms_on_page, function (data) {
            let translationDict = {}
            try {
                data.forEach(function (item, index) {
                    translationDict[terms_on_page[index]] = item;
                });
            } catch (e) {
                console.warn(e);
                translationDict = {}
            }
            callback(translationDict);
        }
    )
}

function processWithTranslationTerms(saved_institutions, callback) {
    if (Object.keys(_translationTerms).length === 0) {
        allTerms(function (terms) {
            _translationTerms = terms;
            callback(saved_institutions, _translationTerms);
        });
    } else {
        callback(saved_institutions, _translationTerms);
    }

}

(function ($) {

        let Course = function (course_dict) {
            this.data = course_dict;
            Object.defineProperty(this, 'checked', {
                get: function () {
                    this.checkbox.checked
                },
                set: function (checked) {
                    this.checkbox.checked = checked;
                }
            })

            Object.defineProperty(this, "id", {
                get: function () {
                    return this.data.uniqueId;
                }
            });

            Object.defineProperty(this, 'elementID', {
                get: function () {
                    return this.id
                }
            });

            Object.defineProperty(this, 'name', {
                get: function () {
                    return this.data.courseName + ' - ' + this.data.uniName;
                }
            });

            Object.defineProperty(this, 'length', {
                get: function () {
                    if (this.hasCourseLength) {
                        return this.data.length + " " + _translationTerms["year_course"]
                    } else {
                        return _translationTerms["course_length_not_available"]
                    }
                }
            });

            Object.defineProperty(this, 'mode', {
                    get: function () {
                        return `${this.data.mode.en.replace(" t", "t")
                            .replace("-t", "t")
                            .replace("time", "Time")}`
                    }
                }
            )

            Object.defineProperty(this, 'query', {
                get: function () {
                    return this.data.uniId + ',' + this.data.courseId + ',' + this.mode;
                }
            });

            Object.defineProperty(this, 'url', {
                get: function () {
                    const _url = this.data.uniId + '/' + this.data.courseId + '/' + this.mode + '/';
                    if (document.documentElement.lang === 'en') {
                        return '/course-details/' + _url
                    } else {
                        return '/cy/course-details/' + _url
                    }
                }
            });

            Object.defineProperty(this, 'hasCourseLength', {
                get: function () {
                    return !(this.data.length === '' || this.data.length === 'None' || this.data === 'None');
                }
            });
        }

        let ComparisonStorage = function comparisonStorage(key, storage_action) {
            this.storage = new StorageControl(key);
            this.storage_action = storage_action;

            Object.defineProperty(this, 'items', {
                get: function () {
                    return this.storage.loadFromStorage();
                },
                set: function (s) {
                    this.storage.writeToStorage(s);
                    this.storage_action(s);
                }
            });
        }

        let StorageControl = function storageControl(key) {
            this.storageKey = key;
            this.loadFromStorage = function () {
                let response = [];
                try {
                    let storage = JSON.parse(localStorage.getItem(this.storageKey));
                    if (!storage) {
                        return response;
                    } else {
                        return storage;
                    }
                } catch (error) {
                    return response
                }
            }

            this.writeToStorage = function (values) {
                if (values) {
                    localStorage.setItem(this.storageKey, JSON.stringify(values));
                }
            }
        }

        let CourseStorage = function courseStorage(key, storage_action) {
            this.storage = new StorageControl(key);
            this.storage_action = storage_action;

            Object.defineProperty(this, 'items', {
                get: function () {
                    return courseObjectsFromStorage(this.storage.loadFromStorage());
                },
                set: function (s) {
                    this.storage.writeToStorage(courseObjectsToStorage(s));
                    this.storage_action(s);

                }
            });

            function courseObjectsToStorage(courses) {
                let to_store = [];
                courses.forEach(function (value, index) {
                        to_store.push(value.data)
                    }
                )
                return to_store;
            }

            function courseObjectsFromStorage(data) {
                let courses_data = data;
                let items = [];
                courses_data.forEach(function (value, index) {
                        let course = new Course(value);
                        items.push(course);
                    }
                )
                return items;
            }
        }

        let CourseView = function courseView(element, course, checked) {
            this.course = course;
            this.checked = checked;
            this.container = element;
            this.isEnglish = location.pathname.indexOf('/cy/') === -1;
            this.courseNameSpan = this.container.querySelector('.bookmark__course-name');
            this.lengthBlock = this.container.querySelector('.bookmark__course-info.length');
            this.courseLengthSpan = this.container.querySelector('.length');
            this.courseModeSpan = this.container.querySelector('.bookmark__course-info.mode .mode');
            this.courseDistanceSpan = this.container.querySelector('.bookmark__course-info.distance .distance');
            this.courseSandwichSpan = this.container.querySelector('.bookmark__course-info.sandwich .sandwich');
            this.courseAbroadSpan = this.container.querySelector('.bookmark__course-info.abroad .abroad');
            this.courseLocationSpan = this.container.querySelector('.bookmark__course-info.location .location');
            this.removeBtn = this.container.querySelector('.bookmark__course-remove');
            this.checkbox = this.container.querySelector('.bookmark-check')
            this.label = this.container.querySelector('.bookmark_label')
            this.update = function () {
                this.checkbox.checked = this.checked;
                this.courseNameSpan.text = this.course.name;
                this.courseLengthSpan.innerHTML = this.course.length;
                if (this.course.length) {
                    if (this.course.length === "1 year course" && this.isEnglish) {
                        this.courseLengthSpan.innerHTML = "12-18 month course"
                    } else if (this.course.length === "1 blwyddyn" && !this.isEnglish) {
                        this.courseLengthSpan.innerHTML = "Cwrs 12-18 mis"
                    } else {
                        this.courseLengthSpan.innerHTML = this.course.length;
                    }
                }
                this.courseLocationSpan.innerHTML = this.course.data.locations;
                if (this.isEnglish) {
                    this.courseModeSpan.innerHTML = this.course.data.mode.en;
                    this.courseDistanceSpan.innerHTML = this.course.data.distance.en;
                    if (this.course.data.distance.en === 0) {
                        this.courseDistanceSpan.innerHTML = "Not Available"
                    }
                    this.courseSandwichSpan.innerHTML = this.course.data.sandwich.en.replace(") }}", "");
                    this.courseAbroadSpan.innerHTML = this.course.data.abroad.en;
                } else {
                    this.courseModeSpan.innerHTML = this.course.data.mode.cy;
                    this.courseDistanceSpan.innerHTML = this.course.data.distance.cy;
                    if (this.course.data.distance.cy === 0) {
                        this.courseDistanceSpan.innerHTML = "Ddim ar gael"
                    }
                    this.courseSandwichSpan.innerHTML = this.course.data.sandwich.cy;
                    this.courseAbroadSpan.innerHTML = this.course.data.abroad.cy;
                }
                this.courseNameSpan.href = this.course.url;
                console.log("MEG", this.courseNameSpan.href)
            }
        }

        function should_enable_how_to(items) {
            if (!items.length) {
                document.getElementById("bookmark__none-selected").style.display = "block";
            } else {
                document.getElementById("bookmark__none-selected").style.display = "none";
            }
        }

        let saved_courses = new CourseStorage('bookmarkedCourses',
            function (items) {
                should_enable_how_to(items);
                window.document.dispatchEvent(BookmarkEvent);
            });

        should_enable_how_to(saved_courses.items);

        let courses_selected_for_comparison = new ComparisonStorage(
            "CoursesForComparison",
            function (items) {
                let compare_button = document.getElementById('compare-courses-button')
                let compare_text = document.getElementById('bookmark-text')
                let courses_selected = document.getElementById('courses-selected')
                const number_selected = items.length;
                if (number_selected >= 1) {
                    courses_selected.innerHTML = "<strong>" + number_selected + " " + _translationTerms["courses_selected"] + "</strong>";
                } else {
                    courses_selected.innerHTML = "";
                }

                if (2 <= number_selected && number_selected <= 7) {
                    compare_button.disabled = false;
                    compare_button.classList.add("enabled");
                    compare_text.innerHTML = _translationTerms["select_up_to_7"];
                    courses_selected.classList.remove("red");
                } else if (7 < number_selected) {
                    courses_selected.classList.add("red");
                    compare_button.classList.remove("enabled");
                    compare_button.disabled = true;
                } else {
                    compare_button.disabled = true;
                    compare_button.classList.remove("enabled");
                    compare_text.innerHTML = _translationTerms["select_at_least_2"];
                }
            });


        processWithTranslationTerms(saved_courses.items, function () {
            addCourseViews(saved_courses.items, document.getElementById("placeholder"));
            courses_selected_for_comparison.storage_action(courses_selected_for_comparison.items);
        });

        function markCourseForComparison(should_store, element_id) {
            const current = courses_selected_for_comparison.items
            saved_courses.items.forEach(function (saved_course, index) {
                if (saved_course.elementID === element_id) {
                    if (should_store) {
                        let compare = {"id": saved_course.id, "rating": 0}
                        current.push(compare);
                        courses_selected_for_comparison.items = current;
                    } else {
                        courses_selected_for_comparison.items = current.filter(function (value, index, arr) {
                            return saved_course.id !== value.id;
                        });
                    }
                }
            });
        }

        function comparisonHandler() {
            markCourseForComparison(this.checked, this.parentElement.id);
        }

        function removeCourseHandler() {
            const container = this.parentElement.parentElement;
            const elementToRemove = this.parentElement.parentElement.id;

            let to_remove = saved_courses.items.filter(function (value, index, arr) {
                return elementToRemove === value.elementID;
            });

            if (container.querySelector(".bookmark-check").checked) {
                removeCoursesFromStorage(courses_selected_for_comparison, to_remove);
            }
            removeCoursesFromStorage(saved_courses, to_remove);
            removeElFromView(elementToRemove);
        }

        function removeCoursesFromStorage(storage, courses) {
            const to_keep = storage.items.filter(function (value, index, atr) {
                let response = false;
                for (let i = 0; i < courses.length; i++) {
                    if (courses[i].id !== value.id) {
                        response = true;
                    }
                }
                return response;
            })
            storage.items = to_keep;
        }

        function removeElFromView(element_id) {
            document.getElementById(element_id).classList.add("hidden");
        }

        function addCourseViews(courses, template) {
            const container = document.getElementById("institution-bookmark");
            container.hidden = false;
            courses.forEach(function (course) {
                const query = course.query;
                const courseTemplate = template.cloneNode(true);
                courseTemplate.id = course.elementID;
                container.appendChild(courseTemplate);
                const el = document.getElementById(course.elementID);
                let checkbox = el.querySelector('.bookmark-check');
                let label = el.querySelector('.bookmark_label');
                checkbox.value = query;
                checkbox.id = query
                label.htmlFor = query
                checkbox.addEventListener("change", comparisonHandler);
                let removeButton = el.querySelector('.bookmark__course-remove');
                removeButton.addEventListener('click', removeCourseHandler);

                let checked = false;
                if (courses_selected_for_comparison.items.some(e => e.id === course.id)) {
                    checked = true;
                }

                let courseView = new CourseView(courseTemplate, course, checked);
                courseView.update();
            })

            const empty = document.getElementById("placeholder");
            container.removeChild(empty);
            document.getElementById('spinner-loading').hidden = true;
        }
    }
    (jQuery)
)
