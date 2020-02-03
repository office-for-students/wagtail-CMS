(function ($) {

    var Filters = function(wrapper, toggle, openBtn) {
        this.wrapper = $(wrapper);
        this.toggle = $(toggle);
        this.openBtn = $(openBtn);
        this.setup();
    }

    Filters.prototype = {
        setup: function() {
            this.closeBtn = this.wrapper.find('.filters-block__cancel-button');
            this.uniFilter = new UniFilter(this.wrapper.find('#uniFilter'));
            this.submitBlock = this.wrapper.find('.filters-block__submit-block');
            this.submitBtn = this.wrapper.find('.filters-block__submit-btn');
            this.inputs = this.wrapper.find('input');
            this.pageInput = this.wrapper.find('#page_input');
            this.countInput = this.wrapper.find('#count_input');
            this.paginationInputs = $('.pagination a');

            this.form = this.wrapper.find('form');

            this.subjectAreaSelector = this.wrapper.find('#subjectArea');
            this.subjectSelector = this.wrapper.find('#subject');
            this.subjectCodeSelector = this.wrapper.find('#subjectCode');
            this.subjectQuery = this.wrapper.find('#subject_query');

            this.postcodeInput = this.wrapper.find('.filters-block__filter-postcode');
            this.distanceInputs = this.wrapper.find('input[name=distance]');
            this.postcodeQuery = this.wrapper.find('#postcode_query');

            this.uniQuery = this.wrapper.find('#institution_query');

            this.startWatcher();
        },

        startWatcher: function()  {
            var that = this;
            this.toggle.click(function() {
                that.wrapper.toggle();
            });

            this.openBtn.click(function() {
                that.wrapper.animate({ "left": 0 }, "slow");
                that.submitBlock.animate({ "left": 0 }, "slow");
            });

            this.closeBtn.click(function() {
                that.wrapper.animate({ "left": '-100%' }, "slow");
                that.submitBlock.animate({ "left": '-100%' }, "slow");
            });

            this.submitBtn.click(function(evt) {
                evt.preventDefault();
                that.prepSubjectQuery();
                that.prepPostcodeQuery();
                that.prepInstitutionQuery();
                that.form.submit();
            });

            for (var i = 0; i < this.inputs.length; i++) {
                $(this.inputs[i]).change(function() {
                    that.submitBtn.removeClass('disabled');
                })
            };

            for (var i = 0; i < this.paginationInputs.length; i++) {
                $(this.paginationInputs[i]).click(function(evt) {
                    evt.preventDefault();
                    that.pageInput.val(this.dataset.page);
                    that.countInput.val(this.dataset.count);
                    that.form.submit();
                });
            }
        },

        prepSubjectQuery: function() {
            var subjectCodes = ""
            if (this.subjectAreaSelector.val() === null && this.subjectSelector.val() === null) {
                subjectCodes = "";
            } else if (this.subjectAreaSelector.val() != null && this.subjectSelector.val() === null) {
                subjectJson = JSON.parse(localStorage.getItem("subjectJSON"));
                for (var i = 0; i < subjectJson.length; i++) {
                    var item = subjectJson[i];
                    if (item.level === "3" && item.code.includes(this.subjectAreaSelector.val())) {
                        subjectCodes += item.code + ","
                    }
                }
            } else {
                subjectCodes = this.subjectCodeSelector[0].value;
            }
            if (subjectCodes !== 'Show all') {
                this.subjectQuery.val(subjectCodes);
            }
        },

        prepPostcodeQuery: function() {
            var postcode = this.postcodeInput.val().replace(' ', '');
            var distance = this.distanceInputs.filter(':checked').val();
            var queryValue = [postcode,  distance].join(',');

            if (postcode && distance) {
                this.postcodeQuery.val(queryValue);
            }
        },

        prepInstitutionQuery: function() {
            var selectedUnis = this.uniFilter.getSelectedUnis();

            if (selectedUnis) {
                this.uniQuery.val(selectedUnis);
            }
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
            var that = this;

            var currentVersion = $('meta[name=currentversion]')[0].content;
            var isCurrentVersionStored = localStorage.getItem("uniJSONVersion") === currentVersion;

            if (!isCurrentVersionStored || localStorage.getItem("uniJSON") === null) {
                $.getJSON("/jsonfiles/institutions", function(result) {
                    localStorage.setItem("uniJSON", JSON.stringify(result));
                    localStorage.setItem("uniJSONVersion", version);

                    that.uniData = result;
                });
            }
            else {
                that.uniData = JSON.parse(localStorage.getItem("uniJSON"))
            }

            that.uniList = new UniList(that.unisListWrapper, that.uniData, that.setTotalCount.bind(that),
                                    that.setSelectedCount.bind(that));
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
        },

        getSelectedUnis: function() {
            return this.uniList.getSelectedUnis();
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
            this.initialSelection = this.listWrapper.data().selectedunis.split(',').filter(Boolean);
            this.renderUnis();
        },

        renderUnis: function() {
            this.unis = [];
            for (var i = 0; i < this.uniData.length; i++) {
                this.unis.push(new Uni(this.uniData[i], this.listWrapper, i, this.selectedSetter, this.initialSelection));
            }
            this.totalSetter(this.unis.length);
            this.selectedSetter(this.initialSelection.length);
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
        },

        getSelectedUnis: function() {
            var selectedUnis = []
            for (var i = 0; i < this.unis.length; i++) {
                var uni = this.unis[i];
                if (uni.isSelected()) {
                    selectedUnis.push('"' + uni.uni.name + '"');
                }
            }
            return selectedUnis.join(',');
        }
    }

    var Uni = function(uniData, parent, index, selectedSetter, initialSelection) {
        this.uni = uniData;
        this.parent = parent;
        this.index = index;
        this.selectedSetter = selectedSetter;
        this.initialSelection = initialSelection;
        this.setup();
    }

    Uni.prototype = {
        setup: function() {
            this.letter = this.uni.alphabet;
            this.id = 'uni-' + this.index;
            this.isPreSelected = $.inArray(this.uni.name, this.initialSelection) !== -1;
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
            inputFieldNode.setAttribute('value', this.uni.name);
            if (this.isPreSelected) {
                inputFieldNode.setAttribute('checked', true);
            }


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
        },

        isSelected: function() {
            return this.uniInput[0].checked;
        }
    }

    function init() {
        var filters = $('.filters-wrapper');
        var toggle = $('.course-finder-results__overview-filter-toggle');
        var openBtn = $('.course-finder-results__overview-filter-open');
        new Filters(filters[0], toggle[0], openBtn[0]);
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
