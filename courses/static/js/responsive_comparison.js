const narrowMarginLeftAndRightClass = "course-info-both";
const wideMarginLeftClass = "course-info-left";
const wideMarginRightClass = "course-info-right";

let currentIndex = 0;

function removeCourseCompare(el) {
    let courseIdToRemove = el.parentElement.parentElement.id;
    let el_index = parseInt(el.parentElement.parentElement.dataset.index);
    let elements = document.getElementsByClassName("cc-column-" + el_index);
    for (let i = 0; 1 <= elements.length; i++) {
        elements[0].remove();
    }

    let local_storage = localStorage.getItem("CoursesForComparison");
    if (local_storage) {
        let storageItems = JSON.parse(local_storage);
        let final = storageItems.slice();
        for (let i = 0; i < storageItems.length; i++) {
            let courseId = storageItems[i].id;
            if (courseId === courseIdToRemove) {
                final.splice(i, 1);
            }
        }

        localStorage.setItem('CoursesForComparison', JSON.stringify(final));

        if (final.length === 0) {
            window.location.reload(true);
        }

        let selectedCount = document.getElementById("numberOfSelected");
        selectedCount.innerHTML = final.length;
    }
    moveIndexToDisplayBy(-1);
}


class ArrowManager {
    leftArrow = document.getElementById("leftArrow");
    rightArrow = document.getElementById("rightArrow");
    centralContainer = document.getElementById("course-info-container");

    removeAllArrows() {
        this.removeBothWideArrows();
        this.removeNarrowArrowsLeftAndRight();
    }

    removeBothWideArrows() {
        this.removeWideArrowLeft();
        this.removeWideArrowRight();
    }

    removeWideArrowLeft() {
        this.centralContainer.classList.remove(wideMarginLeftClass);
        this.leftArrow.classList.remove("single-arrow");
        this.leftArrow.classList.add("hidden");
    }

    removeWideArrowRight() {
        this.centralContainer.classList.remove(wideMarginRightClass);
        this.rightArrow.classList.remove("single-arrow");
        this.rightArrow.classList.add("hidden");
    }

    removeNarrowArrowsLeftAndRight() {
        this.centralContainer.classList.remove(narrowMarginLeftAndRightClass);
        this.rightArrow.classList.add("hidden");
        this.leftArrow.classList.add("hidden");
    }

    includeWideArrowLeft() {
        this.centralContainer.classList.add(wideMarginLeftClass);
        this.leftArrow.classList.remove("hidden");
        this.leftArrow.classList.add("single-arrow");
        this.leftArrow.classList.remove("both-arrows");
    }

    includeWideArrowRight() {
        this.centralContainer.classList.add(wideMarginRightClass);
        this.rightArrow.classList.remove("hidden");
        this.rightArrow.classList.add("single-arrow");
        this.rightArrow.classList.remove("both-arrows");
    }


    includeBothArrows() {
        this.centralContainer.classList.add(narrowMarginLeftAndRightClass);
        this.leftArrow.classList.add("both-arrows");
        this.leftArrow.classList.remove("hidden");
        this.rightArrow.classList.remove("single-arrow");
        this.rightArrow.classList.add("both-arrows");
        this.rightArrow.classList.remove("hidden");
        this.rightArrow.classList.remove("single-arrow");
    }

}

function getValueComparedToMax(value, maximum) {
    if (maximum < value) {
        return maximum;
    } else {
        return value;
    }
}

function getMaxItems(maximum) {
    if (screen.availWidth <= 450 || window.innerWidth <= 450) {
        return getValueComparedToMax(2, maximum);
    } else if (screen.availWidth <= 576 || window.innerWidth <= 576) {
        return getValueComparedToMax(3, maximum);
    } else if (screen.availWidth <= 750 || window.innerWidth <= 750) {
        return getValueComparedToMax(4, maximum);
    } else if (screen.availWidth <= 1140 || window.innerWidth <= 1140) {
        return getValueComparedToMax(5, maximum)
    }

    return maximum;
}

function getColumns() {
    const maxColumns = 7
    const columns = [];
    for (let index = 0; index < maxColumns; index++) {
        let className = "cc-column-" + index;
        let items = document.getElementsByClassName(className);
        if (items.length) {
            columns.push(items);
        }
    }
    return columns;
}

function displayColumn(column, display = false) {
    for (let index = 0; index < column.length; index++) {
        if (display) {
            column.item(index).classList.remove("hidden");
        } else {
            column.item(index).classList.add("hidden");
        }
    }
}

function displayColumnsWithIndex(columns, indexes) {
    for (let index = 0; index < columns.length; index++) {
        if (indexes.includes(index)) {
            displayColumn(columns[index], true);
        } else {
            displayColumn(columns[index])
        }
    }
}

function getNewIndex(increment, max) {
    let new_index = currentIndex + increment;
    if (new_index > max) {
        new_index = max
    }
    if (new_index < 0) {
        new_index = 0;
    }

    return new_index
}

function getCourseIndexesToShow(index, number_of_courses) {
    let indexesToShow = [];
    for (let i = index; i < (index + number_of_courses); i++) {
        indexesToShow.push(i)
    }
    return indexesToShow
}


function updateArrows(indexes, max_columns, number_of_courses) {
    const arrows = new ArrowManager();
    let start = indexes[0]
    const displayingAll = (number_of_courses === indexes.length);
    const hasMoreToDisplay = (start + max_columns < number_of_courses);

    arrows.removeAllArrows();

    if (displayingAll) {
        return;
    }

    if (start === 0 && !displayingAll) {
        arrows.includeWideArrowRight();
    } else if (start > 0 && !hasMoreToDisplay) {
        arrows.includeWideArrowLeft();
    } else {
        arrows.includeBothArrows();
    }
}

function moveIndexToDisplayBy(increment) {
    const columns = getColumns();
    let total_number_of_courses = columns.length
    let new_index = getNewIndex(increment, total_number_of_courses);
    let max_columns = getMaxItems(total_number_of_courses);
    let currentIndexes = getCourseIndexesToShow(new_index, max_columns, total_number_of_courses)
    updateArrows(currentIndexes, max_columns, total_number_of_courses);
    displayColumnsWithIndex(columns, currentIndexes);
    currentIndex = new_index;
    updateStickyHeader();
    showMultipleSubjects();
}

function updateStickyHeader() {
    let element_height = $(".course-detail__course-container").height();
    let accordion_header = $(".sticky-accordion-header");
    accordion_header.css('top', element_height + 20 + "px");
    accordion_header.css('position', "sticky");
    accordion_header.css("z-index", "8");
}

function showMultipleSubjects(){
    let courses = document.getElementsByClassName("course-detail__courses-container");
    let subjectSelector = document.getElementsByClassName("js_subject_wrapper");
    console.log(subjectSelector)
    let response = false;
    for(let i=0; i < courses.length; i++){
        if(courses[i].dataset.multiple_subjects === "True"){
            console.log(courses[i])
            response = true;
        }
    }
    Array.from(subjectSelector).forEach(function(value){
        value.hidden = !response;
    });
}

$(window).on('resize orientationchange', function () {
    currentIndex = 0;
    moveIndexToDisplayBy(0);
});


