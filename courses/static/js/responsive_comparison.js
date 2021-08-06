const narrowMarginLeftAndRightClass = "course-info-both";
const wideMarginLeftClass = "course-info-left";
const wideMarginRightClass = "course-info-right";


let current_index = 0;

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
    const compare_list = JSON.parse(localStorage.getItem("CoursesForComparison"));
    const columns = [];
    if (compare_list) {
        for (let index = 0; index < compare_list.length; index++) {
            let className = "cc-column-" + index;
            columns.push(document.getElementsByClassName(className));
        }
    }
    return columns;
}

function displayColumn(column, display = false) {
    for (var index = 0; index < column.length; index++) {
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
    let new_index = current_index + increment;
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

function updateArrows(active_index, max_columns, total_number_of_courses) {
    const arrows = new ArrowManager();
    arrows.removeAllArrows();
    if (!(max_columns >= total_number_of_courses)) {
        if (active_index + max_columns >= total_number_of_courses) {
            if (max_columns !== total_number_of_courses) {
                arrows.includeWideArrowLeft();
            }
        } else if (active_index === 0) {
            arrows.includeWideArrowRight();
        } else {
            arrows.includeBothArrows();
        }
    }
}

function scrollDisplay(increment) {
    const columns = getColumns();
    let total_number_of_courses = columns.length
    let new_index = getNewIndex(increment, total_number_of_courses);
    let max_columns = getMaxItems(total_number_of_courses);
    updateArrows(new_index, max_columns, total_number_of_courses);
    displayColumnsWithIndex(columns, getCourseIndexesToShow(new_index, max_columns));
    current_index = new_index;
    updateStickyHeader();
}

function updateStickyHeader() {
    let element_height = $(".course-detail__course-container").height();
    let accordion_header = $(".sticky-accordion-header");
    accordion_header.css('top', element_height + 20 + "px");
    accordion_header.css('position', "sticky");
    accordion_header.css("z-index", "8");
}


$(window).on('resize orientationchange', function () {
    current_index = 0;
    scrollDisplay(0);
});

