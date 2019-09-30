(function($){

    var PageDropdowns = function(dropdowns) {
        this.dropdownsList = $(dropdowns);
        this.setup()
    }

    PageDropdowns.prototype = {
        setup: function() {
            this.dropdowns = [];
            this.initialiseDropdowns();
            this.startCloseWatcher();
        },

        initialiseDropdowns: function() {
            for (var i = 0; i < this.dropdownsList.length; i++) {
                this.dropdowns.push(new Dropdown(this.dropdownsList[i], this.closeAll.bind(this)));
            }
        },

        startCloseWatcher: function() {
            var that = this;
            $(document).click(function() {
                that.closeAll();
            });
        },

        closeAll: function(activeSelector) {
            for (var i = 0; i < this.dropdowns.length; i++) {
                this.dropdowns[i].closeOptionList();
            }

            if (activeSelector) {
                activeSelector.openOptionList();
            }
        }
    }

    var Dropdown = function(wrapper, closeCallback) {
        this.wrapper = $(wrapper);
        this.closeCallback = closeCallback;
        this.setup();
    }

    Dropdown.prototype = {
        setup: function() {
            this.baseSelect = this.wrapper.find('select');
            this.options = [];
            this.createUISelect();
        },

        createUISelect: function() {
            var baseSelect = this.baseSelect[0];
            var uiSelect = document.createElement("div");
            uiSelect.setAttribute("class", "select-selected");
            uiSelect.innerHTML = baseSelect.options[baseSelect.selectedIndex].innerHTML;
            this.wrapper.append(uiSelect);
            this.uiSelect = this.wrapper.find('.select-selected');
            this.startWatcher();
            this.createOptionList();
            this.baseSelect.hide();
        },

        createOptionList: function() {
            var baseSelect = this.baseSelect[0];
            var optionList = document.createElement("div");
            optionList.setAttribute("class", "select-items select-hide");
            for (var i = 0; i < baseSelect.length; i++) {
                var optionId = baseSelect.id + '-' + i;
                this.options.push(new DropdownOption(baseSelect[i], optionId, optionList, this.handleSelection.bind(this)));
            }
            this.wrapper.append(optionList)
            this.optionList = this.wrapper.find('.select-items');
        },

        resetOptionList: function() {
            this.optionList.remove();
            this.createOptionList();
            this.uiSelect[0].innerHTML = this.options[0].baseOption[0].innerHTML;
        },

        startWatcher: function() {
            var that = this;

            this.uiSelect.click(function(evt) {
                evt.stopPropagation();
                activeSelector = that;
                if (that.uiSelect.hasClass('select-arrow-active')) {
                    var activeSelector = null;
                }
                that.closeCallback(activeSelector);
            });

            this.baseSelect.on('loadeddata', function() {
                that.resetOptionList();
            })
        },

        openOptionList: function() {
            this.optionList.toggleClass("select-hide");
            this.uiSelect.toggleClass("select-arrow-active");
        },

        closeOptionList: function() {
            this.optionList.addClass("select-hide");
            this.uiSelect.removeClass("select-arrow-active");
        },

        handleSelection: function(selection) {
            for (var i = 0; i < this.baseSelect[0].length; i++) {
                if (this.baseSelect[0][i].innerHTML == selection.baseOption[0].innerHTML) {
                    this.baseSelect[0].selectedIndex = i;
                    this.baseSelect.trigger('change');
                    this.uiSelect[0].innerHTML = selection.baseOption[0].innerHTML;
                    for (var j = 0; j < this.options.length; j++) {
                        this.options[j].unselect();
                    }
                    selection.markSelected();
                }
            }
        }
    }

    var DropdownOption = function(option, index, listContainer, selectionCallback) {
        this.baseOption = $(option);
        this.index = index;
        this.listContainer = $(listContainer);
        this.selectionCallback = selectionCallback;
        this.setup();
    }

    DropdownOption.prototype = {
        setup: function() {
            this.value = this.baseOption[0].text;
            this.createUIOption();
            this.startWatcher();
        },

        createUIOption: function() {
            var uiOption = document.createElement("div");
            uiOption.setAttribute("id", this.index);
            uiOption.setAttribute("class", 'option');
            uiOption.innerHTML = this.baseOption[0].innerHTML;
            if (this.baseOption[0].disabled) {
                uiOption.setAttribute("class", 'select-hide');
            }
            this.listContainer.append(uiOption);
            this.uiOption = this.listContainer.find('#' + this.index);
        },

        startWatcher: function() {
            var that = this;
            this.uiOption.click(function() {
                that.selectionCallback(that);
            })
        },

        unselect: function() {
            this.uiOption.removeClass("same-as-selected");
        },

        markSelected: function() {
            this.uiOption.addClass("same-as-selected");
        }
    }

    function init(){
        var dropdowns = $('[class$=selector]');
        new PageDropdowns(dropdowns);
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))

