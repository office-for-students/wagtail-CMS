class SearchBoxManager {
    dropdown = document.getElementById("myDropdown");
    institutionDropDown = document.getElementById("institutionDropdown");
    rotate = document.getElementById("dropdownChevron")
    searchBar = document.getElementById("institutionSearchBar");
    data = JSON.parse(document.getElementById('search_info').textContent);
    lastInteractionOutside = true;
    list = [];


    setup() {
        let that = this;

        window.addEventListener('click', function (e) {
            if (document.getElementById('myDropdown').contains(e.target)) {
                that.lastInteractionOutside = false;
            } else {
                if (document.getElementById('dropDownPlaceholder').contains(e.target)) {
                    if (that.lastInteractionOutside) {
                        that.showDropDown();
                        that.lastInteractionOutside = false;
                    }
                } else {
                    that.hideDropDown();
                    that.lastInteractionOutside = true;
                }
            }
        });

        this.institutionDropDown.addEventListener("focus", function (event) {
            that.toggleDropDownDisplay();
            that.lastInteractionOutside = !this.lastInteractionOutside;
            that.institutionDropDown.blur();

        });


        Array.from(document.getElementsByClassName('inst-check')).forEach(function (el) {

            el.addEventListener('click', function (event) {
                that.updateDropdownList(event.target);
            })

            if (el.id === "selectMultipleInstitutions") {
                el.addEventListener('click', function (event) {
                    that.selectAll(event.target);
                });
            }
        });

        this.searchBar.addEventListener('keyup', function () {
            that.searchList();
        })
        this.loadExistingSearch();
        this.updateNameOnDropDown();
    }

    toggleDropDownDisplay() {
        if (this.isShowing) {
            this.hideDropDown();
        } else {
            this.showDropDown();
        }
    }

    updateNameOnDropDown() {
        let options_selected = this.data['number_options_selected'];
        if (this.list.length === 0) {
            this.institutionDropDown.innerHTML = this.data['institution_name'];
        } else if (this.list.length === 1) {
            this.institutionDropDown.innerHTML = this.list.join(", ");
        } else {
            this.institutionDropDown.innerHTML = options_selected.replace('{}', this.list.length);
        }
    }

    updateDropdownList(el) {
        const id = el.id;
        const checked = el.checked;

        if (checked && this.list.includes(id) == false && id !== 'selectMultipleInstitutions') {
            this.list.push(id)
        } else if (checked == false && this.list.includes(id)) {
            const index = this.list.indexOf(id);
            this.list.splice(index, 1);
        }

        this.list.sort();

        // previously called populateDropDown at the end
        this.updateNameOnDropDown()
    }


    loadExistingSearch() {
        let institutions_str = this.data['institutions']
        let institution_array = institutions_str ? institutions_str.replace('&#39;', "'") : ""
        let institutions = institution_array.split('@')
        if (institutions) {
            for (let i = 0; i < institutions.length; i++) {
                this.list.push(institutions[i])
            }
        }

        if (this.list[0] == "None" || this.list[0] == "") {
            this.list.pop()
        }

        this.updateNameOnDropDown()
    }

    hideDropDown() {
        this.isShowing = false;
        this.dropdown.classList.remove('show');
        this.institutionDropDown.classList.remove('dropdown-border');
        this.rotate.classList.remove('rotate');
    }

    showDropDown() {
        this.isShowing = true;
        this.dropdown.classList.add('show');
        this.institutionDropDown.classList.add('dropdown-border');
        this.rotate.classList.add('rotate');
        this.searchBar.focus();

    }

    selectAll(source) {
        let aInputs = document.getElementsByTagName('input');
        if (!(document.getElementById("institutionSearchBar").value)) {
            this.list = []
        }

        for (let i = 0; i < aInputs.length; i++) {
            let input = aInputs[i];
            if (input != source && input.className == source.className && input.offsetWidth !== 0) {
                if (source.checked && !(this.list.includes(input.id))) {
                    this.list.push(input.id)
                } else if (!(source.checked)) {
                    const index = this.list.indexOf(input.id);
                    this.list.splice(index, 1);
                }
                input.checked = source.checked;
            }
        }
        this.updateNameOnDropDown()
    }

    searchList() {
        // Declare variables
        let input, filter, institutions, label, txtValue;
        input = document.getElementById("institutionSearchBar");
        filter = input.value.toUpperCase();
        institutions = document.getElementsByClassName("dropdown-content-institution-check");
        const block = document.getElementById("myDropdown");
        const selectAllCheck = document.getElementById("selectAll-check");

        if (filter) {
            selectAllCheck.innerHTML = this.data['select_all_results'];
        } else {
            selectAllCheck.innerHTML = this.data['select_all_institutions'];
        }

        // Loop through all table rows, and hide those who don't match the search query
        for (let i = 0; i < institutions.length; i++) {
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
}

window.document.addEventListener('searchready', function (event) {
    let searchBoxManager = new SearchBoxManager();
    searchBoxManager.setup();
})