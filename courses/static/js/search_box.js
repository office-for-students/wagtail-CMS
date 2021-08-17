document.addEventListener("click", toggleDropdown);

function toggleDropdown(event) {
    var dropdown = document.getElementById("myDropdown");
    var border = document.getElementById("institutionDropdown")
    var rotate = document.getElementById("dropdownChevron")

    if (!(event.target.classList.contains('drop-item'))) {
        dropdown.classList.remove('show');
        border.classList.remove("dropdown-border");
        rotate.classList.remove("rotate");
    }
}

function openDropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
    document.getElementById("institutionSearchBar").focus();
    document.getElementById("institutionDropdown").classList.toggle("dropdown-border");
    document.getElementById("dropdownChevron").classList.toggle("rotate");
}

var lastClick = null;
$(document).ready(function () {
    $('#institutionDropdown').mousedown(function (e) {
        lastClick = e.target;
    }).focus(function (e) {
        if (e.target == lastClick) {
            openDropdown();
        } else {
            openDropdown();
        }
        lastClick = null;
        $("#institutionDropdown").blur();
    });
});

var list = []

function dropdownName(id, checked) {
    var dropdown = document.getElementById("institutionDropdown");

    if (checked && list.includes(id) == false && id !== 'selectMultipleInstitutions') {
        list.push(id)
    } else if (checked == false && list.includes(id)) {
        const index = list.indexOf(id);
        list.splice(index, 1);
    }

    list.sort()

    populateDropDown(dropdown, list);

}

function dropdownLoad() {
    var dropdown = document.getElementById("institutionDropdown");
    var institution_array = "{{filter_form.institutions}}".replace('&#39;', "'")
    var institutions = institution_array.split('@')
    if (institutions) {
        for (i = 0; i < institutions.length; i++) {
            list.push(institutions[i])
        }
    }

    if (list[0] == "None" || list[0] == "") {
        list.pop()
    }

    populateDropDown(dropdown, list);

}

function populateDropDown(dropdown, list) {
    var options_selected = "{% get_translation key='number_options_selected' language=page.get_language %}"
    if (list.length === 0) {
        dropdown.innerHTML = "{% get_translation key='institution_name' language=page.get_language %}";
    } else if (list.length === 1) {
        dropdown.innerHTML = list.join(", ");
    } else {
        dropdown.innerHTML = options_selected.replace('{}', list.length);
    }
}

function selectAll(source) {
    var aInputs = document.getElementsByTagName('input');
    if (!(document.getElementById("institutionSearchBar").value)) {
        list = []
    }

    for (var i = 0; i < aInputs.length; i++) {
        if (aInputs[i] != source && aInputs[i].className == source.className && aInputs[i].offsetWidth !== 0) {
            if (source.checked && !(list.includes(aInputs[i].id))) {
                list.push(aInputs[i].id)
            } else if (!(source.checked)) {
                const index = list.indexOf(aInputs[i].id);
                list.splice(index, 1);
            }
            aInputs[i].checked = source.checked;
        }
    }
}


function searchList() {
    // Declare variables
    var input, filter, institutions, label, i, txtValue, selectMultiple;
    input = document.getElementById("institutionSearchBar");
    filter = input.value.toUpperCase();
    institutions = document.getElementsByClassName("dropdown-content-institution-check");
    block = document.getElementById("myDropdown");
    selectAllCheck = document.getElementById("selectAll-check");

    if (filter) {
        selectAllCheck.innerHTML = "{% get_translation key='select_all_results' language=page.get_language %}"
    } else {
        selectAllCheck.innerHTML = "{% get_translation key='select_all_institutions' language=page.get_language %}"
    }

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < institutions.length; i++) {
        label = institutions[i].getElementsByTagName("label")[0];
        if (label) {
            txtValue = label.textContent || label.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                institutions[i].style.display = "block";
            } else {
                institutions[i].style.display = "none";
            }
            if (txtValue.toUpperCase().indexOf(filter).length < 5) {
                block.style.overflowY = "hidden"
            }
        }
    }
}
