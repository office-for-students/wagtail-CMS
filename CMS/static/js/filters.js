(function ($) {

    var Filters = function(wrapper, toggle) {
        this.wrapper = $(wrapper);
        this.toggle = $(toggle);
        this.setup();
    }

    Filters.prototype = {
        setup: function() {
            this.closeBtn = this.wrapper.find('.filters-block__cancel-button');
            this.uniFilter = new UniFilter(this.wrapper.find('#uniFilter'));

            this.startWatcher();
        },

        startWatcher: function()  {
            var that = this;
            this.toggle.click(function() {
                that.wrapper.toggle();
            });

            this.closeBtn.click(function() {
                that.wrapper.hide();
            })
        }
    }

    var UniFilter = function(wrapper) {
        this.wrapper = wrapper;
        this.setup();
    }

    UniFilter.prototype = {
        setup: function() {
            this.unisListWrapper = this.wrapper.find('.filters-block__filter-uni-list');
            this.selectAllBtn = this.wrapper.find('.filters-block__filter-uni-controls-select');
            this.clearAllBtn = this.wrapper.find('.filters-block__filter-uni-controls-clear');
            this.selectedCountSpace = this.wrapper.find('.selected');
            this.totalCountSpace = this.wrapper.find('.total');

            this.initialiseAlphabetToggles();
            this.loadUnis();
            this.startWatchers();
        },

        startWatchers: function() {
            this.selectAllBtn.click(this.handleSelectAll.bind(this));
            this.clearAllBtn.click(this.handleClearAll.bind(this));
        },

        initialiseAlphabetToggles: function() {
            var letters = this.wrapper.find('.filters-block__filter-uni-alphabet-input');
            this.alphabetToggles = [];
            for (var i = 0; i  < letters.length; i++) {
                this.alphabetToggles.push(new AlphabetToggle(letters[i], this.handleLetterChange.bind(this)));
            }
        },

        loadUnis: function() {
            if (sessionStorage.getItem("uniJSON") === null) {
                $.getJSON("/static/jsonfiles/institutions.json", function(result) {
                    result.sort(function(a, b) {
                        if(a.order_by_name < b.order_by_name) { return -1; }
                        if(a.order_by_name > b.order_by_name) { return 1; }
                        return 0;
                    });
                })

                sessionStorage.setItem("uniJSON", JSON.stringify(result));
                this.uniData = result;
            } else {
                this.uniData = JSON.parse(sessionStorage.getItem("uniJSON"))
            }

            this.uniList = new UniList(this.unisListWrapper, this.uniData, this.setTotalCount.bind(this),
                                        this.setSelectedCount.bind(this));
        },

        handleLetterChange: function(filterLetter) {
            this.uniList.updateList(filterLetter);
        },

        handleSelectAll: function() {
            this.uniList.selectAll();
        },

        handleClearAll: function() {
            this.uniList.clearAll();
        },

        setTotalCount: function(count) {
            this.totalCountSpace[0].innerText = count;
        },

        setSelectedCount: function(count, change) {
            if (count !== null) {
                this.selectedCountSpace[0].innerText = count;
            } else {
                var current = parseInt(this.selectedCountSpace[0].innerText);
                this.selectedCountSpace[0].innerText = current + change;
            }
        }
    }

    var AlphabetToggle = function(input, callback) {
        this.input = input;
        this.callback = callback;
        this.setup();
    }

    AlphabetToggle.prototype = {
        setup: function() {
            this.letter = this.input.value;
            this.startWatcher();
        },

        startWatcher: function() {
            var that = this;

            $(this.input).change(function() {
                if (this.checked) {
                   that.callback(that.letter);
                }
            })
        }
    }

    var UniList = function(listWrapper, uniData, totalSetter, selectedSetter) {
        this.listWrapper = listWrapper;
        this.uniData = uniData;
        this.totalSetter = totalSetter;
        this.selectedSetter = selectedSetter;
        this.setup();
    }

    UniList.prototype = {
        setup: function() {
            this.renderUnis();
        },

        renderUnis: function() {
            this.unis = [];
            for (var i = 0; i < this.uniData.length; i++) {
                this.unis.push(new Uni(this.uniData[i], this.listWrapper, i, this.selectedSetter));
            }
            this.totalSetter(this.unis.length);
        },

        updateList: function(filterLetter) {
            for (var i = 0; i < this.unis.length; i++) {
                var uni = this.unis[i];
                if (uni.letter === filterLetter) {
                    uni.show();
                } else {
                    uni.hide();
                }
            }
        },

        selectAll: function() {
            for (var i = 0; i < this.unis.length; i++) {
                var uni = this.unis[i];
                uni.select();
            }
            this.selectedSetter(this.unis.length);
        },

        clearAll: function() {
            for (var i = 0; i < this.unis.length; i++) {
                var uni = this.unis[i];
                uni.clear();
            }
            this.selectedSetter(0);
        }
    }

    var Uni = function(uniData, parent, index, selectedSetter) {
        this.uni = uniData;
        this.parent = parent;
        this.index = index;
        this.selectedSetter = selectedSetter;
        this.setup();
    }

    Uni.prototype = {
        setup: function() {
            this.letter = this.uni.alphabet;
            this.id = 'uni-' + this.index;
            this.createUni();
        },

        createUni: function() {
            var uniWrapperNode = document.createElement('div');
            uniWrapperNode.classList.add('filters-block__filter-uni-item');
            uniWrapperNode.setAttribute('data-letter', this.uni.alphabet);
            uniWrapperNode.setAttribute('id', this.id);

            var labelWrapperNode = document.createElement('label');
            labelWrapperNode.classList.add('filters-block__filter-uni');
            labelWrapperNode.classList.add('checkbox');

            var labelNode = document.createElement('span');
            labelWrapperNode.classList.add('filters-block__filter-uni-item-label');
            var uniName = document.createTextNode(this.uni.name);
            labelNode.appendChild(uniName);

            var inputFieldNode = document.createElement('input');
            inputFieldNode.classList.add('filters-block__filter-uni-item-input');
            inputFieldNode.setAttribute('id', this.uni.order_by_name);
            inputFieldNode.setAttribute('type', 'checkbox');
            inputFieldNode.setAttribute('name', 'unis');
            inputFieldNode.setAttribute('value', this.uni.name);

            var checkboxNode = document.createElement('span');
            checkboxNode.classList.add('checkmark');

            labelWrapperNode.appendChild(labelNode);
            labelWrapperNode.appendChild(inputFieldNode);
            labelWrapperNode.appendChild(checkboxNode);

            uniWrapperNode.appendChild(labelWrapperNode);

            this.parent.append(uniWrapperNode);
            this.uniWrapper = this.parent.find('#' + this.id);
            this.uniInput = this.uniWrapper.find('input');
            this.startWatcher();
        },

        startWatcher: function() {
            var that = this;
            this.uniInput.change(function() {
                if (this.checked) {
                    that.selectedSetter(null, 1);
                } else {
                    that.selectedSetter(null, -1);
                }
            })
        },

        show: function() {
            this.uniWrapper.show();
        },

        hide: function() {
            this.uniWrapper.hide();
        },

        select: function() {
            this.uniInput[0].checked = true;
        },

        clear: function() {
            this.uniInput[0].checked = false;
        }
    }

    function init() {
        var filters = $('.filters-wrapper');
        var toggle = $('.course-finder-results__overview-filter-toggle');
        new Filters(filters[0], toggle[0]);
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
