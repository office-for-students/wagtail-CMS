(function ($) {

    var Filters = function(wrapper, toggle, openBtn) {
        this.wrapper = $(wrapper);
        this.toggle = $(toggle);
        this.openBtn = $(openBtn);
        this.setup();
    };

    Filters.prototype = {
        setup: function() {
            this.closeBtn = this.wrapper.find('.filters-block__cancel-button');
            // this.uniFilter = new UniFilter(this.wrapper.find('#uniFilter'));
            this.submitBlock = this.wrapper.find('.filters-block__submit-block');
            this.submitBtn = this.wrapper.find('.filters-block__submit-btn');
            this.inputs = this.wrapper.find('input');
            this.pageInput = this.wrapper.find('#page_input');
            this.countInput = this.wrapper.find('#count_input');
            this.paginationInputs = $('.pagination a');
            this.languageChgBtnList = $('#language_select');

            this.form = this.wrapper.find('.filters-block__form');

            this.subjectAreaSelector = this.wrapper.find('#subjectArea');
            this.subjectSelector = this.wrapper.find('#subject');
            this.subjectCodeSelector = this.wrapper.find('#subjectCode');
            this.subjectQuery = this.wrapper.find('#subject_query');

            this.postcodeInput = this.wrapper.find('.filters-block__filter-postcode');
            this.distanceInputs = this.wrapper.find('input[name=distance]');
            this.postcodeQuery = this.wrapper.find('#postcode_query');
            this.qualificationInputs = this.wrapper.find('input[name=qualification]');
            this.qualificationQuery = this.wrapper.find('#qualification_query');

            this.uniQuery = this.wrapper.find('#institution_query');
            this.courseQuery = this.wrapper.find('#course_query');

            var lastSearch = JSON.stringify(this.form.serializeArray());

            sessionStorage.setItem("lastSearch", lastSearch);

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
                document.getElementById("sort_by_subject").value = false
                // that.prepSubjectQuery();
                // that.prepPostcodeQuery();
                // that.prepInstitutionQuery();
                // that.prepQualificationQuery();
                that.pageInput.val(1);
                that.form.submit();
            });

            for (var i = 0; i < this.inputs.length; i++) {
                $(this.inputs[i]).change(function() {
                    that.submitBtn.removeClass('disabled');
                })
            };

            for (var i = 0; i < this.languageChgBtnList.length; i++) {
                $(this.languageChgBtnList[i]).click(function(evt) {
                    evt.preventDefault();
                    // that.prepSubjectQuery();
                    // that.prepPostcodeQuery();
                    // that.prepInstitutionQuery();
                    // that.prepQualificationQuery();
                    that.form.attr('action', $(this).attr("href"));
                    that.form.submit();
                });
            }

            for (var i = 0; i < this.paginationInputs.length; i++) {
                $(this.paginationInputs[i]).click(function(evt) {
                    evt.preventDefault();
                    that.pageInput.val(this.dataset.page);
                    that.countInput.val(this.dataset.count);
                    that.form.attr('action', $(this).attr("href"));
                    that.form.submit();
                });
            }
        },

        prepSubjectQuery: function() {
            var subjectCodes = "";
            if (this.subjectAreaSelector.val() === null && this.subjectSelector.val() === null) {
                subjectCodes = "";
            } else if (this.subjectAreaSelector.val() != null && this.subjectSelector.val() === null) {
                subjectJson = JSON.parse(localStorage.getItem("subjectsJSON"));
                for (var i = 0; i < subjectJson.length; i++) {
                    var item = subjectJson[i];
                    if (item.level === "3" && item.code.includes(this.subjectAreaSelector.val())) {
                        subjectCodes += item.code + ","
                    }
                }
            } else {
                subjectCodes = this.subjectCodeSelector[0].value;
            }
            if (subjectCodes !== 'Show all' && subjectCodes !== 'Dangos popeth') {
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

        prepQualificationQuery: function() {
            var selectedQualifications = [];

            this.qualificationInputs.each( function()  {
                if ( this.checked ) {
                    selectedQualifications.push(this.value);
                }
            });

            this.qualificationQuery.val(selectedQualifications);
        },



        prepInstitutionQuery: function() {
            var selectedUnis = this.uniFilter.getSelectedUnis();

            if (selectedUnis) {
                this.uniQuery.val(selectedUnis);
            }
        }
    };

    var UniFilter = function(wrapper) {
        this.wrapper = wrapper;
        this.setup();
    };

    UniFilter.prototype = {
        setup: function() {
            this.unisListWrapper = this.wrapper.find('.filters-block__filter-uni-list');
            this.selectAllBtn = this.wrapper.find('.filters-block__filter-uni-controls-select');
            this.clearAllBtn = this.wrapper.find('.filters-block__filter-uni-controls-clear');
            this.selectedCountSpace = this.wrapper.find('.selected');
            this.totalCountSpace = this.wrapper.find('.total');

            this.initialiseAlphabetToggles();
            this.loadUnis();
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

            var language = $('meta[name=pagelanguage]')[0].content;
            var currentVersion = $('meta[name=currentversion]')[0].content;
            var isCurrentVersionStored = localStorage.getItem("uniJSONVersion_" + language) === currentVersion;

            if (!isCurrentVersionStored || localStorage.getItem("uniJSON_" + language) === null) {
                $.getJSON("/jsonfiles/institutions/" + language + "/", function(result) {
                    localStorage.setItem("uniJSON_" + language, JSON.stringify(result));
                    localStorage.setItem("uniJSONVersion_" + language, currentVersion);

                    that.uniData = result;
                    that.finishInit();
                });
            }
            else {
                that.uniData = JSON.parse(localStorage.getItem("uniJSON_" + language))
                that.finishInit();
            }
        },

        finishInit: function() {
            this.uniList = new UniList(this.unisListWrapper, this.uniData, this.setTotalCount.bind(this),
                this.setSelectedCount.bind(this));

            this.startWatchers();
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
    };

    var AlphabetToggle = function(input, callback) {
        this.input = input;
        this.callback = callback;
        this.setup();
    };

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
    };

    var UniList = function(listWrapper, uniData, totalSetter, selectedSetter) {
        this.listWrapper = listWrapper;
        this.uniData = uniData;
        this.totalSetter = totalSetter;
        this.selectedSetter = selectedSetter;
        this.setup();
    };

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
    };

    var Uni = function(uniData, parent, index, selectedSetter, initialSelection) {
        this.uni = uniData;
        this.parent = parent;
        this.index = index;
        this.selectedSetter = selectedSetter;
        this.initialSelection = initialSelection;
        this.setup();
    };

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
            if (this.isPreSelected) {
                this.uniInput[0].checked = true;
            }
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
    };

    function init() {
        var filters = $('.filters-wrapper');
        var toggle = $('.course-finder-results__overview-filter-toggle');
        var openBtn = $('.course-finder-results__overview-filter-open');

        new Filters(filters[0], toggle[0], openBtn[0]);
    }

    $(document).on('page:load', init);
    $(init)

}(jQuery));

function toggleDistance(distance_checked, campus_checked) {
    var disable_countries = $('input[name=countries_check]');
    var disable_radio = $('input[name=location_radio]');
    var disable_postcode = $('.postcode-fieldset')
    var distance_checked_mobile = document.getElementsByClassName('distance')[1].checked;
    var campus_checked_mobile = document.getElementsByClassName('campus')[1].checked;
    // form duplicates when in mobile view so the Id cannot be used.
    if(window.innerWidth > 576){
        if(distance_checked && campus_checked == false){
            $(".message").css( "display", "block" )
            disable_countries.attr('disabled', 'disabled');
            disable_radio.attr('disabled', 'disabled');
            disable_postcode.attr('disabled', 'disabled');
            disable_postcode.css('border', '1px solid grey');
            $(".distance-dropdown").css("pointer-events", "none");
            $('.filters-block__submit-btn').prop('disabled', false);
            $('.filters-block__submit-btn').css('background-color', "#8e3b74");
        }
        else{
            $(".message").css( "display", "none" )
            disable_countries.attr('disabled', false);
            disable_radio.attr('disabled', false);
            disable_postcode.attr('disabled', false);
            $(".distance-dropdown").css("pointer-events", "auto");

            if($('[name="distance"]').val() && $('[name="postcode"]').val()){
                $('.filters-block__submit-btn').prop('disabled', false);
                $('.filters-block__submit-btn').css('background-color', "#8e3b74");
            }
            else if($('.filters-block__filter-radio-postcode').is(":checked") && ($('[name="postcode"]').val() !== $('[name="distance"]').val())){
                $('.filters-block__submit-btn').css('background-color', "grey");
                $('.filters-block__submit-btn').prop('disabled', true);
            }

            if(!($('[name="postcode"]').val()) && $('[name="distance"]').val()){
                $('[name="postcode"]').css( "border", "1px solid red" )
            }

            if(!($('[name="distance"]').val()) && $('[name="postcode"]').val()){
                $('.distance-dropdown').css( "border", "1px solid red" )
            }
        }
    }
    else{
        if(distance_checked_mobile && campus_checked_mobile == false){
            $(".message").css( "display", "block" )
            disable_countries.attr('disabled', 'disabled');
            disable_radio.attr('disabled', 'disabled');
            disable_postcode.attr('disabled', 'disabled');
            $('.filters-block__submit-btn').prop('disabled', false);
            $('.filters-block__submit-btn').css('background-color', "#8e3b74");

        }
        else {
            $(".message").css( "display", "none" )
            disable_countries.attr('disabled', false);
            disable_radio.attr('disabled', false);
            disable_postcode.attr('disabled', false);
            $(".distance-dropdown").css("pointer-events", "auto");

            if($('[name="distance"]').val() && $('[name="postcode"]').val()){
                $('.filters-block__submit-btn').prop('disabled', false);
                $('.filters-block__submit-btn').css('background-color', "#8e3b74");
            }
            else if($('.filters-block__filter-radio-postcode').is(":checked") && ($('[name="postcode"]').val() !== $('[name="distance"]').val())){
                $('.filters-block__submit-btn').css('background-color', "grey");
                $('.filters-block__submit-btn').prop('disabled', true);
            }

            if(!($('[name="postcode"]').val()) && $('[name="distance"]').val()){
                $('[name="postcode"]').css( "border", "1px solid red" )
            }

            if(!($('[name="distance"]').val()) && $('[name="postcode"]').val()){
                $('.distance-dropdown').css( "border", "1px solid red" )
            }
        }
    }
}

// a function to trigger each hidden checkbox. This hidden input is what is submitted to the FilterForm. Using this means we can keep the value of the checkbox if distance learning is selected, submitted and then removed
function toggleCheckbox(country) {
    var shown = document.getElementsByClassName(country);
    var hidden = document.getElementsByClassName('hidden-' + country);
    if(window.innerWidth > 576){
        if(shown[0].checked){
           hidden[0].checked = true;
        }
        else{
           hidden[0].checked = false;
        }
    }
    else{
        if(shown[1].checked){
           hidden[1].checked = true;
        }
        else{
           hidden[1].checked = false;
        }
    }
}

function selectDistance(id){
    var dropdownText = $(".filters-block__filter-postcode-div-dropdown-text");
    var distanceValue = $('[name="distance"]');

        if(id !== ""){
            dropdownText.text(translation.replace("{}", id))
        }
        else{
            dropdownText.text("")
        }

    distanceValue.val(id);
    distanceValue.trigger('change');
}

$(document).ready(function() {
   $('input[type="radio"]').click(function() {
       if($(this).attr('id') == 'region') {
            $('.region-div').css( "display", "block" );
            $('.filters-block__filter-postcode-div').css( "display", "none" );
            $('[name="countries_query"]').prop('disabled', false);
            $('[name="distance"]').prop('disabled', true);
            $('[name="postcode"]').prop('disabled', true);
            $('.filters-block__submit-btn').prop('disabled', false);
            $('.filters-block__submit-btn').css('background-color', "#8e3b74");
        }

       else if($(this).attr('id') == 'postcode') {
            $('.region-div').css( "display", "none" );
            $('.filters-block__filter-postcode-div').css( "display", "flex" );
            $('[name="countries_query"]').prop('disabled', true);
            $('[name="distance"]').prop('disabled', false);
            $('[name="postcode"]').prop('disabled', false);

            if(($('[name="postcode"]').val() && $('[name="distance"]').val())){
                $('.filters-block__submit-btn').prop('disabled', false);
                $('.filters-block__submit-btn').css('background-color', "#8e3b74");
            }
            else if($('[name="postcode"]').val() !== $('[name="distance"]').val()){
                $('.filters-block__submit-btn').prop('disabled', true);
                $('.filters-block__submit-btn').css('background-color', "grey");
            }
            else{
                $('.filters-block__submit-btn').prop('disabled', false);
                $('.filters-block__submit-btn').css('background-color', "#8e3b74");
            }
        }
    });
});

$(document).ready(function() {
   $('.postcode-fieldset').change(function() {
        if(window.innerWidth > 576){
            var postcode = $('[name="postcode"]')[0]
        }
        else{
            var postcode = $('[name="postcode"]')[1]
        }
        if(postcode.value && $('[name="distance"]').val()){
            $('.filters-block__submit-btn').prop('disabled', false);
            $('.filters-block__submit-btn').css('background-color', "#8e3b74");
        }
        else if(postcode.value === $('[name="distance"]').val()){
            $('.filters-block__submit-btn').prop('disabled', false);
            $('.filters-block__submit-btn').css('background-color', "#8e3b74");
        }
        else if(postcode.value !== $('[name="distance"]').val()){
            $('.filters-block__submit-btn').prop('disabled', true);
            $('.filters-block__submit-btn').css('background-color', "grey");
        }
        if(!(postcode.value) && $('[name="distance"]').val()){
            $('[name="postcode"]').css( "border", "1px solid red" )
        }
        else{
            $('[name="postcode"]').css( "border", "1px solid #595959" )
        }
        if(!($('[name="distance"]').val()) && postcode.value){
            $('.distance-dropdown').css( "border", "1px solid red" )
        }
        else{
            $('.distance-dropdown').css( "border", "1px solid #595959" )
        }
    });
});


//Check on load whether the postcode radio button is checked and then display the postcode div if true.
//Make sure borders of inputs aren't red as these will have to be prefilled anyway.
$(document).ready(function() {
    if($('.filters-block__filter-radio-postcode').is(":checked")){
        $('.region-div').css( "display", "none" );
        $('.filters-block__filter-postcode-div').css( "display", "flex" );
        $('[name="countries_query"]').prop('disabled', true);
        $('[name="distance"]').prop('disabled', false);
        $('[name="postcode"]').prop('disabled', false);
        $('.filters-block__submit-btn').prop('disabled', false);
        $('.filters-block__submit-btn').css('background-color', "#8e3b74");
    }
});
//function to check whether distance is checked on page load and to disable the location filters if it is.
$(document).ready(function() {
    var disable_input = $('input[name=countries_check]');
    var disable_radio = $('input[name=location_radio]');
    if($('.distance').is(":checked") == true && $('.campus').is(":checked") == false){
        disable_input.attr('disabled', 'disabled');
        disable_radio.attr('disabled', 'disabled')
        $(".message").css( "display", "block" )
    }
});

$(document).ready(function(){
    $('#clear-filters').click(function(){
        $('.filters-block__filter-radio-region').prop('checked', true)
        $('#countries-england').prop('checked', false);
        $('#countries-ireland').prop('checked', false);
        $('#countries-scotland').prop('checked', false);
        $('#countries-wales').prop('checked', false);
        $('[name="distance"]').val('')
        $('[name="postcode"]').val('')

        $('#mode-full-time').prop('checked', false);
        $('#mode-part-time').prop('checked', false);
        $('#mode-distance').prop('checked', false);
        $('#mode-campus').prop('checked', false);

        $('#course_query').val('');
        $('#institutions_query').val('');
        $('.inst-chk').prop('checked', false);

        for (filter_base_name of ['placement', 'foundation', 'abroad']) {
            $('#'+filter_base_name+'-yes').prop('checked', false);
            $('#'+filter_base_name+'-no').prop('checked', false);
            $('#'+filter_base_name+'-either').prop('checked', false);
        }

        $('#subjectArea option:eq(0)').prop('selected','selected');
        $('#subject option:eq(0)').prop('selected','selected');
        $('#subjectCode option:eq(0)').prop('selected','selected');
        $('#subject_query').val('');

        $('#sort_by_subject').val(false);

        $('#postcode_field').val('');
        $("#one").prop('checked', false);
        $("#two").prop('checked', false);
        $("#three").prop('checked', false);
        $('#postcode_query').val('');

        $("#first_degree").prop('checked', false);
        $("#other_undergraduate").prop('checked', false);

        $('.filters-block__filter-uni-alphabet-input').prop('checked', false);
        $(".filters-block__filter-uni-list").html("");

        $('.filters-block__form').first().submit();
    });
});