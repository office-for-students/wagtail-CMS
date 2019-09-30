(function($){

    var SearchDropdown = function(container) {
        this.container = $(container);
        this.minSearchTermLength = 3;
        this.setup()
    }

    SearchDropdown.prototype = {
        setup: function() {
            this.selectionField = this.container.find('.selection-field');
            this.fieldName = this.selectionField[0].name;
            this.searchField = $(this.container.find('.search-field-input')[0]);
            this.optionList = $(this.container.find('.options-list'));
            this.placeholder = $(this.optionList.find('.placeholder'));
            this.initialiseSelect();
            this.watchForFocus();
            this.watchForSearchTerm();
        },

        initialiseSelect: function() {
            var that = this;
            $.each(JSON.parse(localStorage.getItem("uniJSON")), function(index, item) {
                var optionId = that.fieldName + '-' + index;
                var optionValue = '"' + item.name + '"';

                var option = document.createElement("option");
                option.setAttribute("id", optionId);
                option.setAttribute("value", optionValue);
                option.innerHTML = item.name;
                that.selectionField.append(option);
            });
            this.selectOptions = this.selectionField.find('option');
            this.initialiseOptions();
        },

        initialiseOptions: function() {
            this.options = []
            for (var i = 0; i < this.selectOptions.length; i++) {
                this.options.push(new SearchOption(this.selectOptions[i], this.optionList, this.handleSelection.bind(this)));
            }
        },

        watchForFocus: function() {
            var that = this;
            this.searchField.focus(function() {
                that.optionList.show();
            });

            $(document).click(function(e) {
                if (!that.container[0].contains(e.target)) {
                  that.optionList.hide();
                }
            });
        },

        watchForSearchTerm: function() {
            var that = this;
            this.searchField.keyup(function(e) {
                if (e.target.value.length >= that.minSearchTermLength) {
                    that.placeholder.hide();
                    that.filterOptionsList(e.target.value);
                } else {
                    that.placeholder.show();
                    that.clearFilter();
                }
            });
        },

        clearFilter: function() {
            for (var i = 0; i < this.options.length; i++) {
                this.options[i].hideOption();
            }
        },

        clearSearch: function() {
            this.searchField[0].value = '';
            this.clearFilter();
        },

        filterOptionsList: function(searchTerm) {
            var searchTerm = searchTerm.toLowerCase();
            for (var i = 0; i < this.options.length; i++) {
                this.options[i].filterForSearch(searchTerm, this.selectionField.value);
            }
        },

        handleSelection: function(option) {
            this.clearSearch();
            this.searchField[0].value = option.textValue;
            this.optionList.hide();
        }
    }

    var SearchOption = function(option, wrapper, handleSelectionCallback) {
        this.option = option;
        this.wrapper = wrapper;

        this.handleSelection = handleSelectionCallback;
        this.setup();
    }

    SearchOption.prototype = {
        setup: function() {
            this.textValue = this.option.innerText;
            this.id = this.option.id;
            this.idValue = this.option.value;

            this.createUIOption();
            this.watchForSelection();
        },

        createUIOption: function() {
            var uiOption = document.createElement("div");
            uiOption.setAttribute("id", this.id);
            uiOption.setAttribute("class", 'option');
            uiOption.innerHTML = this.textValue;
            this.wrapper.append(uiOption);
            this.uiOption = this.wrapper.find('#' + this.id);
            if (this.option.disabled) {
                this.uiOption.hide();
            }
        },

        watchForSelection: function() {
            var that = this;
            $(this.uiOption).click(function(e) {
                that.option.selected = true;
                that.handleSelection(that);
            })
        },

        filterForSearch: function(searchTerm, selectedOptions) {
            if (this.textValue.toLowerCase().indexOf(searchTerm) > -1) {
                $(this.uiOption).show();
            } else {
                $(this.uiOption).hide();
            }
        },

        hideOption: function() {
            $(this.uiOption).hide();
        }
    }

    function init(){
        var searchDropdowns = $('.search-dropdown');
        for (var i = 0; i < searchDropdowns.length; i++) {
            new SearchDropdown(searchDropdowns[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
