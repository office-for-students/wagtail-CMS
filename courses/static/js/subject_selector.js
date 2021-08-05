function removeSelected(element) {
    let parent = element.target.parentElement
    console.log(parent.children)
    if (parent.children.length > 1) {
        for (let i = 0; i < parent.children.length; i++) {
            parent.children[i].classList.remove("selected");
        }
    }
}

function setEventListeners() {
    let parents = document.getElementsByTagName("OL");
    for (let i = 0; i < parents.length; i++) {
        parents[i].addEventListener("click", function (e) {
            removeSelected(e);
            e.target.classList.add("selected");
        });
    }
}