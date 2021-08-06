function displayData(element) {
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

function handleSelected(element) {
    let parent = element.target.parentElement;
    console.log(element.children)
    if (parent.children.length > 1) {
        for (let i = 0; i < parent.children.length; i++) {
            parent.children[i].classList.remove("selected");
        }
    }
    displayData(element)
}

function setEventListeners() {
    let parents = document.getElementsByTagName("OL");
    for (let i = 0; i < parents.length; i++) {
        parents[i].addEventListener("click", function (e) {
            handleSelected(e);
            e.target.classList.add("selected");
        });
    }
}