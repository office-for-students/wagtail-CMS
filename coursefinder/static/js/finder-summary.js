(function ($) {

    var SummaryPage = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    SummaryPage.prototype = {
        setup: function() {
            this.btn = this.wrapper.find('.course-finder-content__next-button');
            this.form = this.wrapper.find('form');

            this.initialiseView();
            this.startWatchers();
        },

        initialiseView: function() {
            var that = this;

            if (sessionStorage.getItem("countries")) {
                var countries = sessionStorage.getItem("countries")
                $('#countries').text(countries.split(",").join(", "))
            }

            if (sessionStorage.getItem("modes")) {
                var modes = sessionStorage.getItem("modes")
                $('#modes').text(modes.split(",").join(", "))
            }

            if (sessionStorage.getItem("subject")) {
                var subjects = sessionStorage.getItem("subject")
                var subjectNames = []
                subjectsArray = subjects.split(",")

                $.each(subjectsArray, function(index, subject) {
                    subjectsArray[index] = subject.replace(/"/g, '');
                })

                $.each(JSON.parse(localStorage.getItem("subjectsJSON")), function(index, a) {
                    $.each(subjectsArray, function(index, b) {
                        if(a.code === b) {
                            subjectNames.push(that.getSubjectName(a));
                        }
                    })
                })
                $('#subjects').text(subjectNames.join(', '));
            }

            if (sessionStorage.getItem("uni")) {
                var uni = sessionStorage.getItem("uni")
                $('#narrow').text(uni.split(",").join(", "))
            }

            if (sessionStorage.getItem("postcode")) {
                var postcode = sessionStorage.getItem("postcode")
                $('#narrow').text(postcode.split(",").join(", "))
            }
        },

        getSubjectName: function(item) {
            if (location.href.indexOf('/cy/') === -1) {
                return item.english_name;
            } else {
                return item.welsh_name;
            }
        },

        startWatchers: function() {
            var that = this;

            this.btn.click(function() {
                var subject_query = sessionStorage.getItem('subjectCodes')
                var institution_query = sessionStorage.getItem('uni')
                var mode_query = sessionStorage.getItem('modes')
                var countries_query = sessionStorage.getItem('countries')
                var postcode_query = sessionStorage.getItem('postcode')

                $("input[name='subject_query']").val(subject_query)
                $("input[name='institution_query']").val(institution_query)
                $("input[name='mode_query']").val(mode_query)
                $("input[name='countries_query']").val(countries_query)
                $("input[name='postcode_query']").val(postcode_query)
                that.form.submit();
            });
        }
    }

    function init() {
        var summaryPages = $('.template-course-finder-summary');
        new SummaryPage(summaryPages[0]);
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
