var bottom_display = 0;
var items = document.getElementsByClassName("arrow")

const slide_left = document.getElementById("slideLeft");
const slide_right = document.getElementById("slideRight");
const course_info_container = document.getElementById("course-info-container")
if(screen.availWidth <= 320 || window.innerWidth <= 320){
    var small_screen_amount = 1
}
else{
    var small_screen_amount = 2
}

function hideCourses(){
    for(var i=0; i < items.length; i++){
        for (var index = 0; index < compare_list.length; index ++){

            var course_info = document.getElementById(items[i].id)
            var course_div = document.getElementById(`courseContainer-${index}`);

            if(screen.availWidth <= 576 ||screen.availWidth <= 576){
                if(+course_div.dataset.index > bottom_display + small_screen_amount || +course_div.dataset.index < bottom_display){
                    course_div.classList.add("hidden");
                }
                else{
                    course_div.classList.remove("hidden");
                }
                if(+course_info.dataset.index > bottom_display + small_screen_amount || +course_info.dataset.index < bottom_display){
                    course_info.classList.add("hidden");
                }
                else{
                    course_info.classList.remove("hidden");
                }
            }
            else if(window.innerWidth <= 576 ||window.innerWidth <= 576){
                if(+course_div.dataset.index > bottom_display + small_screen_amount || +course_div.dataset.index < bottom_display){
                    course_div.classList.add("hidden");
                }
                else{
                    course_div.classList.remove("hidden");
                }
                if(+course_info.dataset.index > bottom_display + small_screen_amount || +course_info.dataset.index < bottom_display){
                    course_info.classList.add("hidden");
                }
                else{
                    course_info.classList.remove("hidden");
                }
            }
            else{
                course_div.classList.remove("hidden");
                course_info.classList.remove("hidden");
            }
        }
    }
}

function scrollDisplay(){
    if(bottom_display + small_screen_amount + 1 === compare_list.length){
        slide_right.classList.add("hidden");
        course_info_container.classList.remove("course-info-right");
    }
    else{
        slide_right.classList.remove("hidden");
        course_info_container.classList.add("course-info-right");
    }

    if(bottom_display === 0){
        slide_left.classList.add("hidden");
        course_info_container.classList.remove("course-info-both", "course-info-left");
    }
    else{
        slide_left.classList.remove("hidden");
        course_info_container.classList.add("course-info-left");
    }
    if(!(slide_left.classList.contains("hidden")) && !(slide_right.classList.contains("hidden"))){
        slide_left.classList.remove("single-arrow");
        slide_right.classList.remove("single-arrow");
        slide_left.classList.add("both-arrows");
        slide_right.classList.add("both-arrows");
        course_info_container.classList.remove("course-info-left", "course-info-right");
        course_info_container.classList.add("course-info-both");
    }
    else{
        slide_left.classList.add("single-arrow");
        slide_right.classList.add("single-arrow");
        slide_left.classList.remove("both-arrows");
        slide_right.classList.remove("both-arrows");
        course_info_container.classList.remove("course-info-both");
    }

    hideCourses();
}

function smallScreenDisplay(){
    if(bottom_display === 0){
        slide_left.classList.add("hidden");
    }
    if(screen.availWidth >= 576 || window.innerWidth >= 576){
        course_info_container.classList.remove("course-info-right");
        course_info_container.classList.remove("course-info-left");
        course_info_container.classList.remove("course-info-both");
    }
    else if(!(slide_left.classList.contains("hidden")) && slide_right.classList.contains("hidden")){
        course_info_container.classList.add("course-info-left");
    }
    else if(!(slide_right.classList.contains("hidden")) && slide_left.classList.contains("hidden")){
        course_info_container.classList.add("course-info-right");
    }
    else if(!(slide_right.classList.contains("hidden")) && !(slide_left.classList.contains("hidden"))){
        course_info_container.classList.remove("course-info-right");
        course_info_container.classList.remove("course-info-left");
        course_info_container.classList.add("course-info-both");
    }

    hideCourses();
}



$(window).on('resize orientationchange load', function(){
    smallScreenDisplay();
});