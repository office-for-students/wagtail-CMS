(function($){

    var SubjectSelector = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup()
    }

    SubjectSelector.prototype = {
        setup: function() {
            console.log(0)
            this.subjectAreaSelector = this.wrapper.find('#subjectArea');
            this.subjectSelector = this.wrapper.find('#subject');
            this.subjectCodeSelector = this.wrapper.find('#subjectCode');

            this.loadSubjectData();
            this.startWatchers();
        },

        loadSubjectData: function() {
            console.log(5)
            var that = this;
            if (sessionStorage.getItem("subjectJSON") === null) {
                $.getJSON("/static/jsonfiles/subject-codes.json", function(result) {
                    result.sort(function(a, b){
                        if (a.englishname < b.englishname) { return -1; }
                        if (a.englishname > b.englishname) { return 1; }
                        return 0;
                    });

                    sessionStorage.setItem("subjectJSON", JSON.stringify(result));

                    that.subjectData = result;
                })
            } else {
                this.subjectData = JSON.parse(sessionStorage.getItem("subjectJSON"));
            }
            this.initialiseSelectors();
        },

        initialiseSelectors: function() {
            console.log(10)
            for (var i = 0; i < this.subjectData.length; i++) {
                var item = this.subjectData[i];

                if(item.level === "1") {
                    this.subjectAreaSelector.append(`<option value='${item.code}'>${item.englishname}</option>`)
                }

                if(item.level === "2") {
                    this.subjectSelector.append(`<option value='${item.code}'>${item.englishname}</option>`)
                }

                if(item.level === "3") {
                    this.subjectCodeSelector.append(`<option data-code='${item.code}' value='${item.englishname}'>${item.englishname}</option>`)
                }
            }

            this.subjectOptions = this.subjectSelector.find('option');
            this.subjectCodeOptions = this.subjectCodeSelector.find('option');
        },

        startWatchers: function() {
            var that = this;

            this.subjectAreaSelector.change(this.handleAreaSelection.bind(this));

            this.subjectSelector.change(this.handleSubjectSelection.bind(this));
        },

        handleAreaSelection: function() {
            for (var i = 0; i < this.subjectOptions.length; i++) {
                var option = this.subjectOptions[i];
                $(option).removeAttr("disabled");
                if (!option.value.includes(this.subjectAreaSelector[0].value)) {
                    $(option).attr("disabled", "disabled");
                }
            }
            this.subjectSelector.trigger('loadeddata');
        },

        handleSubjectSelection: function() {
            var all = ''
            for (var i = 0; i < this.subjectCodeOptions.length; i++) {
                var option = this.subjectCodeOptions[i];
                $(option).attr("disabled", "disabled");
                if (option.dataset.code.includes(this.subjectSelector[0].value)) {
                    $(option).removeAttr("disabled");
                    all += '"' + option.value + '",';
                }
            }
            this.subjectCodeOptions[0].value = all;

            this.subjectCodeSelector.removeClass('hidden');
            this.subjectCodeSelector.addClass('visible');

            this.subjectCodeSelector.trigger('loadeddata');
        }
    }

    function init() {
        console.log('init')
        var selectorsWrapper = $('.subject-picker');
        console.log(selectorsWrapper)
        for (var i = 0; i < selectorsWrapper.length; i++) {
            new SubjectSelector(selectorsWrapper[0]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))

