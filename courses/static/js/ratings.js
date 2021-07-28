function toggle_icon(icon_id) {
    var icon_name = "#" + icon_id;
    $(icon_name).toggleClass("fa-plus");
    $(icon_name).toggleClass("fa-minus");
}

function removeCourseCompare(index) {
    const compare_list = JSON.parse(localStorage.getItem("compareCourses"));
    compare_list.splice(index, 1);
    localStorage.setItem('compareCourses', JSON.stringify(compare_list));

    var checkbox = document.getElementById("course" + index);
    const form = document.getElementById("compareForm");
    checkbox.checked = false;

    form.submit();
}

window.addEventListener("load", function () {
    const compare_list = JSON.parse(localStorage.getItem("compareCourses"));
    var saved_institutions = JSON.parse(localStorage.getItem("comparisonCourses"));
    // var add_courses_link = document.getElementById("addCoursesLink")
    var add_courses_button = document.getElementById("addCourses")
    var id_list = [];
    var hidden_check = document.getElementById("hiddenCourseCompare");
    if (hidden_check) {
        if (compare_list) {
            for (var i = 0; i < compare_list.length; i++) {
                id_list.push(compare_list[i].id);
            }

            var index = 0
            for (var i = 0; i < saved_institutions.length; i++) {
                let courseId = saved_institutions[i].courseId
                let query = saved_institutions[i].uniId + ',' + courseId + ',' + saved_institutions[i].mode.en

                if (id_list.includes(courseId)) {
                    hidden_check.innerHTML += `<input id="${'course' + index}" type="checkbox" value="${query}" name="courses" hidden checked>`
                    index++
                }
            }

            if (compare_list.length === 7) {
                // add_courses_link.href = "";
                add_courses_button.disabled = true;
                add_courses_button.style.backgroundColor = "grey";
            }

            for (var index = 0; index < compare_list.length; index++)
                for (var i = 1; i <= compare_list[index].rating; i++) {
                    var star = document.getElementById("course-" + index + "-star" + i);
                    star.innerHTML = "★";
                    star.classList.add("orange");
                }
        }
    }
});

function addStarRating(id, value, index) {

    const compare_list = JSON.parse(localStorage.getItem("compareCourses"));
    var star = document.getElementById(id);

    if (+value > compare_list[index].rating) {
        for (var i = 1; i <= value; i++) {
            var star_fill = document.getElementById("course-" + index + "-star" + i);
            star_fill.innerHTML = "★";
            star_fill.classList.add("orange");
        }
        compare_list[index].rating = +value
    } else if (+value < compare_list[index].rating) {
        for (var i = 3; i > +value; i--) {
            var star_fill = document.getElementById("course-" + index + "-star" + i);
            star_fill.innerHTML = "☆";
            star_fill.classList.remove("orange");
        }
        compare_list[index].rating = +value
    } else if (+value == compare_list[index].rating) {
        for (var i = 3; i > +value; i--) {
            var star_fill = document.getElementById("course-" + index + "-star" + i);
            star_fill.innerHTML = "☆";
            star_fill.classList.remove("orange");
        }
        compare_list[index].rating = +value - 1
    }


    localStorage.setItem('compareCourses', JSON.stringify(compare_list));
}

function hoverStars(value, index) {
    const compare_list = JSON.parse(localStorage.getItem("compareCourses"));
    if (+value < compare_list[index].rating) {
        for (var i = 3; i > +value; i--) {
            var star = document.getElementById("course-" + index + "-star" + i);
            star.innerHTML = "☆";
            star.classList.remove("orange");
        }
    } else if (+value > 0) {
        for (var i = 1; i <= value; i++) {
            var star = document.getElementById("course-" + index + "-star" + i);
            star.innerHTML = "★";
            star.classList.add("orange");
        }
    }
}

function mouseExitStars(index) {
    const compare_list = JSON.parse(localStorage.getItem("compareCourses"));
    for (var i = 1; i <= 3; i++) {
        var star = document.getElementById("course-" + index + "-star" + i);
        if (i <= compare_list[index].rating) {
            star.innerHTML = "★";
            star.classList.add("orange");
        } else {
            star.innerHTML = "☆";
            star.classList.remove("orange");
        }
    }
}