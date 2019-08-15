(function($){

    var SearchDropdown = function(container) {
        this.container = $(container);
        this.minSearchTermLength = 3;
        this.setup()
    }

    SearchDropdown.prototype = {
        setup: function() {
            this.selectionField = this.container.find('.selection-field')[0];
            this.searchField = $(this.container.find('.search-field-input')[0]);
            this.optionList = $(this.container.find('.options-list'));
            this.placeholder = $(this.optionList.find('.placeholder'));
            this.initialiseOptions();
            this.watchForFocus();
            this.watchForSearchTerm();
        },

        initialiseOptions: function() {
        var that = this;
            $.each(JSON.parse(sessionStorage.getItem("uniJSON")), function(index, item) {
              that.optionList.append(`<option value='${item.name}'>${item.name}</option>`)
            });

            this.options = []
            var options = this.optionList.find('option');
            for (var i = 0; i < options.length; i++) {
                this.options.push(new SearchOption(options[i], this.handleSelection.bind(this)));
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
            this.selectionField.value = option.idValue;
            this.searchField[0].value = option.textValue;
            this.optionList.hide();
        }
    }

    var SearchOption = function(option, handleSelectionCallback) {
        this.option = option;
        this.textValue = option.innerText;
        this.idValue = option.value;
        this.handleSelection = handleSelectionCallback;
        this.setup();
    }

    SearchOption.prototype = {
        setup: function(){
            this.watchForSelection();
        },

        watchForSelection: function() {
            var that = this;
            $(this.option).click(function(e) {
                that.handleSelection(that);
            })
        },

        filterForSearch: function(searchTerm, selectedOptions) {
            if (this.textValue.toLowerCase().indexOf(searchTerm) > -1) {
                $(this.option).show();
            } else {
                $(this.option).hide();
            }
        },

        hideOption: function() {
            $(this.option).hide();
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
