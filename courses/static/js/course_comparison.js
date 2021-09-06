class ScrollListener {
    lastActionPosition = 0
    actionAdjustment = 0
    lastPosition = 0
    forwardAction = null;
    reverseAction = null;

    constructor(forwardAction, reverseAction, adjustment, triggerElement = null) {
        this.forwardAction = forwardAction;
        this.reverseAction = reverseAction;
        this.actionAdjustment = adjustment;
        this.triggerY = triggerElement;
    }

    movingForward(position, lastPosition) {
        return (position > lastPosition);
    }

    isTimerForAction(position, adjustment, last_action, forward = true) {
        if (forward) {
            const actionPoint = adjustment + last_action
            return (position >= actionPoint)
        } else {
            const actionPoint = last_action - (adjustment);
            return (position <= actionPoint)
        }
    }

    callActionForDirection(position, is_forward) {
        if (is_forward) {
            this.forwardAction(position);
        } else {
            this.reverseAction(position);

        }
    }

    updatePosition(position) {
        const rect = this.triggerY.getBoundingClientRect();
        if (rect.top <= 0) {
            const isForward = this.movingForward(position, this.lastPosition);
            if (this.isTimerForAction(position, this.actionAdjustment, this.lastActionPosition, isForward)) {
                this.callActionForDirection(position, isForward);
                this.lastActionPosition = position;
            }
        } else {
            this.reverseAction(position);
        }
        this.lastPosition = position
    }
}

class ScrollManager {
    ticking = false;
    listeners = [];
    keys = [];
    lastPosition = 0

    constructor() {
        const that = this;
        document.addEventListener('scroll', function (e) {
            that.lastPosition = window.scrollY > 0 ? window.scrollY : 0;

            if (!that.ticking) {
                window.requestAnimationFrame(function () {
                    that.updateListeners(that.lastPosition);
                    that.ticking = false;
                });

                that.ticking = true;
            }
        });
    }

    add(object, key) {
        if (this.keys.hasOwnProperty(key)) {
            throw 'Item for key already added';
        }
        this.keys.push(key);
        this.listeners.push(object);
    }

    remove(key) {
        if (this.keys.hasOwnProperty(key)) {
            let index = this.keys.indexOf(key)
            this.keys.splice(index, 1);
            this.listeners.splice(index, 1);
        }
    }

    updateListeners(position) {
        this.listeners.forEach(function (item) {
                item.updatePosition(position);
            }
        )
    }
}


class RatingsManager {

    valueAndIndexForElement(el) {
        let index = el.id.split("-")[1];
        let value = el.value;

        return [parseInt(index), parseInt(value), el.parentElement.parentElement.id]
    }

    valueAndIndexFor(event) {
        return this.valueAndIndexForElement(event.target)
    }

    setStars() {
        const comparisonCourses = this.getCoursesForComparison();
        for (let i = 0; i < comparisonCourses.length; i++) {
            for (let starIndex = 1; starIndex < 4; starIndex++) {
                if (comparisonCourses[i].rating > starIndex) {
                    let star = document.getElementById("course-" + i + "-star" + starIndex);
                    star.innerHTML = "★";
                    star.classList.add("orange");
                }
            }
        }
    }

    setupView() {
        this.setEventListener();
        this.setStars();
    }

    setEventListener() {
        const manager = this
        let ratingsContainers = document.getElementsByClassName('js-star-rating');
        Array.from(ratingsContainers).forEach(function (el) {
            el.addEventListener("mouseover", function (event) {
                let [index, value, elementID] = manager.valueAndIndexFor(event)
                manager.hoverStars(value, index, elementID);

            })

            el.addEventListener("mouseleave", function (event) {
                let [index, value, elementID] = manager.valueAndIndexFor(event)
                manager.mouseExitStars(value, index, elementID);
            })

            el.addEventListener('click', function (event) {
                let [index, value, elementId] = manager.valueAndIndexFor(event)
                manager.addStarRating(value, index, elementId);
            })
        })
    }

    getCoursesForComparison() {
        return JSON.parse(localStorage.getItem("CoursesForComparison"));
    }

    getCourseForID(element_id) {
        const compare_list = this.getCoursesForComparison();

        let selectCourse = null;

        compare_list.forEach(function (course) {
            if (course.id === element_id) {
                selectCourse = course;
            }
        })
        return selectCourse
    }

    addStarRating(value, index, element_id) {
        const compare_list = this.getCoursesForComparison();
        let selectedCourse = this.getCourseForID(element_id)
        const currentRating = selectedCourse.rating;
        if (currentRating > value) {
            if (currentRating - 1 === 1) {
                value = 0;
            }
        }
        compare_list.forEach(function (course) {
            if (course.id === selectedCourse.id) {
                course.rating = value === 0 ? value : value + 1;
                course.rating = value === 0 ? value : value + 1;
            }
        })
        localStorage.setItem('CoursesForComparison', JSON.stringify(compare_list));
    }


    hoverStars(value, index, element_id) {
        let selectedCourse = this.getCourseForID(element_id)
        if (value < selectedCourse.rating) {
            for (let i = 3; i > value; i--) {
                let star = document.getElementById("course-" + index + "-star" + i);
                star.innerHTML = "☆";
                star.classList.remove("orange");
            }
        } else if (value > 0) {
            for (let i = 1; i <= value; i++) {
                let star = document.getElementById("course-" + index + "-star" + i);
                star.innerHTML = "★";
                star.classList.add("orange");
            }
        }
    }


    mouseExitStars(value, index, element_id) {
        let selectedCourse = this.getCourseForID(element_id)
        for (let i = 1; i <= 3; i++) {
            let star = document.getElementById("course-" + index + "-star" + i);
            if (i <= selectedCourse.rating - 1) {
                star.innerHTML = "★";
                star.classList.add("orange");
            } else {
                star.innerHTML = "☆";
                star.classList.remove("orange");
            }
        }
    }
}

class ArrowManager {
    narrowMarginLeftAndRightClass = "course-info-both";
    wideMarginLeftClass = "course-info-left";
    wideMarginRightClass = "course-info-right";

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
        this.centralContainer.classList.remove(this.wideMarginLeftClass);
        this.leftArrow.classList.remove("single-arrow");
        this.leftArrow.classList.add("hidden");
    }

    removeWideArrowRight() {
        this.centralContainer.classList.remove(this.wideMarginRightClass);
        this.rightArrow.classList.remove("single-arrow");
        this.rightArrow.classList.add("hidden");
    }

    removeNarrowArrowsLeftAndRight() {
        this.centralContainer.classList.remove(this.narrowMarginLeftAndRightClass);
        this.rightArrow.classList.add("hidden");
        this.leftArrow.classList.add("hidden");
    }

    includeWideArrowLeft() {
        this.centralContainer.classList.add(this.wideMarginLeftClass);
        this.leftArrow.classList.remove("hidden");
        this.leftArrow.classList.add("single-arrow");
        this.leftArrow.classList.remove("both-arrows");
    }

    includeWideArrowRight() {
        this.centralContainer.classList.add(this.wideMarginRightClass);
        this.rightArrow.classList.remove("hidden");
        this.rightArrow.classList.add("single-arrow");
        this.rightArrow.classList.remove("both-arrows");
    }


    includeBothArrows() {
        this.centralContainer.classList.add(this.narrowMarginLeftAndRightClass);
        this.leftArrow.classList.add("both-arrows");
        this.leftArrow.classList.remove("hidden");
        this.rightArrow.classList.remove("single-arrow");
        this.rightArrow.classList.add("both-arrows");
        this.rightArrow.classList.remove("hidden");
        this.rightArrow.classList.remove("single-arrow");
    }

}

class ComparisonDisplayManager {
    arrowManager = null;
    onChange = null;
    currentIndex = 0;

    constructor(arrowManager, scrollManager, onchange) {
        this.scrollManager = scrollManager;
        this.arrowManager = arrowManager;
        this.setEventListeners();
        this.onChange = onchange;
    }

    setEventListeners() {
        const that = this;
        this.arrowManager.leftArrow.addEventListener("click", function () {
            that.moveIndexToDisplayBy(-1);
        });
        this.arrowManager.rightArrow.addEventListener("click", function () {
            that.moveIndexToDisplayBy(1);
        })

        const removeCourseButtons = document.querySelectorAll('*[id^="ratings_remove"]');
        Array.from(removeCourseButtons).forEach(function (value) {
            value.addEventListener("click", function (el) {
                that.removeCourseCompare(el.target)
            })
        });
        window.addEventListener('resize', function () {
            that.moveIndexToDisplayBy(0);
        })

        window.addEventListener('orientationchange', function () {
            that.moveIndexToDisplayBy(0);
        })
    }

    removeCourseCompare(el) {
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

            let lastIndex = storageItems.length - 2
            Array.from(document.getElementsByClassName(`info-box-${lastIndex}`)).forEach(function (el) {
                el.classList.remove("left")
                el.classList.add("right")
            })

            localStorage.setItem('CoursesForComparison', JSON.stringify(final));

            if (final.length === 0) {
                window.location.reload(true);
            }

            let selectedCount = document.getElementById("numberOfSelected");
            let selectedCountMob = document.getElementById("numberOfSelected-mob")
            selectedCount.innerHTML = final.length;
            selectedCountMob.innerHTML = final.length;
        }
        this.moveIndexToDisplayBy(-1);
    }


    getValueComparedToMax(value, maximum) {
        if (maximum < value) {
            return maximum;
        } else {
            return value;
        }
    }

    getMaxItems(maximum) {
        if (screen.availWidth <= 450 || window.innerWidth <= 450) {
            return this.getValueComparedToMax(2, maximum);
        } else if (screen.availWidth <= 576 || window.innerWidth <= 576) {
            return this.getValueComparedToMax(3, maximum);
        } else if (screen.availWidth <= 750 || window.innerWidth <= 750) {
            return this.getValueComparedToMax(4, maximum);
        } else if (screen.availWidth <= 1140 || window.innerWidth <= 1140) {
            return this.getValueComparedToMax(5, maximum)
        }

        return maximum;
    }

    getColumns() {
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

    displayColumn(column, display = false) {
        for (let index = 0; index < column.length; index++) {
            if (display) {
                column.item(index).classList.remove("hidden");
            } else {
                column.item(index).classList.add("hidden");
            }
        }
    }

    displayColumnsWithIndex(columns, indexes) {
        for (let index = 0; index < columns.length; index++) {
            if (indexes.includes(index)) {
                this.displayColumn(columns[index], true);
            } else {
                this.displayColumn(columns[index])
            }
        }
    }

    getNewIndex(increment, max) {
        let new_index = this.currentIndex + increment;
        if (new_index > max) {
            new_index = max
        }
        if (new_index < 0) {
            new_index = 0;
        }

        return new_index
    }

    getCourseIndexesToShow(index, number_of_courses, total_number_of_courses) {
        if (number_of_courses === total_number_of_courses) {
            index = 0;
        }

        let indexesToShow = [];
        for (let i = index; i < (index + number_of_courses); i++) {
            indexesToShow.push(i)
        }
        return indexesToShow
    }


    updateArrows(indexes, max_columns, number_of_courses) {
        let arrows = this.arrowManager;
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

    moveIndexToDisplayBy(increment) {
        const columns = this.getColumns();
        let total_number_of_courses = columns.length
        let new_index = this.getNewIndex(increment, total_number_of_courses);
        let max_columns = this.getMaxItems(total_number_of_courses);
        let currentIndexes = this.getCourseIndexesToShow(new_index, max_columns, total_number_of_courses)
        this.updateArrows(currentIndexes, max_columns, total_number_of_courses);
        this.displayColumnsWithIndex(columns, currentIndexes);
        this.currentIndex = new_index;
        this.updateStickyHeader();
        this.onChange();
    }

    updateStickyHeader(force_top = false) {
        const element = document.getElementById("course-cards-container");
        let style = getComputedStyle(element);
        let accordion_header = $(".sticky-accordion-header");
        if (!force_top) {
            accordion_header.css('top', parseInt(style.height) - 2 + "px");
        } else {
            accordion_header.css('top', parseInt(style.paddingTop) - 2 + "px");
        }
        accordion_header.css('position', "sticky");
        accordion_header.css("z-index", "8");
    }

}

class InfoBoxManager {

    constructor() {
        this.addLeft();
        this.setListeners();
    }

    toggleHidden(el) {
        el.classList.toggle("hidden");
    }

    addLeft() {
        Array.from(document.getElementsByClassName("information-text info-box-0")).forEach(function (el) {
            el.classList.add("info-left");
        })

    }

    setListeners() {
        let infoIcon = document.getElementsByClassName("information-icon");
        let infoText = document.getElementsByClassName("information-text");
        for (let i = 0; i < infoIcon.length; i++) {
            let that = this;
            let icon = infoIcon[i];
            let text = infoText[i];
            icon.addEventListener("mouseover", function () {
                that.toggleHidden(text);
            })
            icon.addEventListener("mouseout", function () {
                that.toggleHidden(text);
            })
        }
    }
}

class MultipleSubjectsManager {

    setup() {
        this.showMultipleSubjects();
        this.setEventListeners()
    }

    showMultipleSubjects() {
        let courses = document.getElementsByClassName("course-detail__courses-container");
        let subjectSelector = document.getElementsByClassName("js_subject_wrapper");
        let response = false;
        for (let i = 0; i < courses.length; i++) {
            if (courses[i].dataset.multiple_subjects === "True") {
                response = true;
            }
        }
        Array.from(subjectSelector).forEach(function (value) {
            value.hidden = !response;
        });
    }

    displayData(element) {
        let index = element.target.dataset.details.split(",");
        let title = index[0]
        let column = index[1];
        let dataIndex = index[2];
        let toBeShown = document.getElementsByClassName(`column-${column}${title} item-${dataIndex}`);
        let toBeHidden = document.getElementsByClassName(`column-${column}${title}`);

        for (let i = 0; i < toBeHidden.length; i++) {
            let el = toBeHidden[i];
            el.hidden = true;
        }
        for (let x = 0; x < toBeShown.length; x++) {
            toBeShown[x].hidden = false;
        }
    }

    handleSelected(element) {
        let parent = element.target.parentElement;
        if (parent.children.length > 1) {
            for (let i = 0; i < parent.children.length; i++) {
                parent.children[i].classList.remove("selected");
            }
        }
        this.displayData(element)
    }

    setEventListeners() {
        let parents = document.getElementsByTagName("OL");
        let manager = this;
        for (let i = 0; i < parents.length; i++) {
            parents[i].addEventListener("click", function (e) {
                manager.handleSelected(e);
                e.target.classList.add("selected");
            });
        }
    }
}

class SubAccordionManager{

    constructor(){
        this.setEventListeners();
    }

    toggleAccordion(title, index){
        let expand = document.getElementById(`${title}-${index}-expand`)
        let collapse = document.getElementById(`${title}-${index}-collapse`)
        let accordionBody = document.getElementById(`${title}-${index}`)

        expand.classList.toggle("hidden")
        collapse.classList.toggle("hidden")
        accordionBody.classList.toggle("hidden")
    }

    setEventListeners() {
        let subAccordions = document.getElementsByClassName("sub_accordion_header")
        for (let i = 0; i < subAccordions.length; i++) {
            const that = this
            let title = subAccordions[i].id
            let index = subAccordions[i].dataset.index
            subAccordions[i].addEventListener("click", function(){
                that.toggleAccordion(title, index)
            })
        }
    }
}


function setupView() {
    let scrollManager = new ScrollManager();

    function areCardsOnDisplay(cards){
        let style = getComputedStyle(cards).display;
        return true ? style == "block" : false
    }

    let arrowManager = new ArrowManager();
    arrowManager.removeAllArrows();
    let subAccordionManager = new SubAccordionManager();
    let multipleSubjectsManager = new MultipleSubjectsManager();
    let courseRatingsManager = new RatingsManager();
    let infoBoxManager = new InfoBoxManager();
    courseRatingsManager.setupView();
    multipleSubjectsManager.setup();
    let courseComparison = new ComparisonDisplayManager(arrowManager, scrollManager, function () {
        multipleSubjectsManager.showMultipleSubjects();
    });
    courseComparison.moveIndexToDisplayBy(0);
    let animateTime = 192;
    let cards = document.getElementById('course-cards-container');
    const cardsRect = cards.getBoundingClientRect()
    let tabletop = document.getElementById("ac-1");
    let scrollListener = new ScrollListener(function (position) {
            cards.classList.add('cards-hide');
            setTimeout(function () {
                courseComparison.updateStickyHeader(areCardsOnDisplay(cards));
            }, animateTime);
        }, function (position) {
            cards.classList.remove('cards-hide');
            setTimeout(function () {
                courseComparison.updateStickyHeader();
            }, animateTime);
        },
        cardsRect.height,
        tabletop
    );

    scrollManager.add(scrollListener, "header");
}

$(window).on('load', function () {
    const AccordionsEvent = new Event('build-accordions');
    const SearchReadyEvent = new Event('searchready')

    function generateURLParams() {
        let local_storage = localStorage.getItem("CoursesForComparison");
        let array = [];
        if (local_storage) {
            array = JSON.parse(local_storage);
        }
        let list = []
        array.forEach(function (value, index) {
            list.push(value.id);
        })
        return list.join('&courses=');
    }

    function numberOfStored() {
        let saved = [];
        if (localStorage.getItem("bookmarkedCourses"))
            saved = JSON.parse(localStorage.getItem("bookmarkedCourses"));
        return saved.length
    }

    function showComparison(callback) {
        let request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status >= 200 && this.status && this.status < 300) {
                callback(this.responseText, (this.status !== 206));

            }
        };

        if (document.documentElement.lang === "cy") {
            request.open("GET", "/cy/ajax/course-comparison/?courses=" + generateURLParams() + '&hasStorage=' + numberOfStored(), true);
        } else {
            request.open("GET", "/ajax/course-comparison/?courses=" + generateURLParams() + '&hasStorage=' + numberOfStored(), true);
        }
        request.send();
    }

    showComparison(function (response, run_js = false) {
        document.getElementById("comparison-body").innerHTML = response;
        if (run_js) {
            setupView();
            document.dispatchEvent(AccordionsEvent);
        } else {
            document.dispatchEvent(SearchReadyEvent);
        }
    });
});