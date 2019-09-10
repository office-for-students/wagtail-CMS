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
            if (sessionStorage.getItem("countries") != null) {
                var countries = sessionStorage.getItem("countries")
                $('#countries').text(countries.split(",").join(", "))
            }

            if (sessionStorage.getItem("modes") != null) {
                var modes = sessionStorage.getItem("modes")
                $('#modes').text(modes.split(",").join(", "))
            }

            if (sessionStorage.getItem("subject") != null) {
                var subjects = sessionStorage.getItem("subject")
                var subjectNames = []
                subjectsArray = subjects.split(",")

                $.each(subjectsArray, function(index, subject) {
                    subjectsArray[index] = subject.replace(/"/g, '');
                })

                $.each(JSON.parse(localStorage.getItem("subjectJSON")), function(index, a) {
                    $.each(subjectsArray, function(index, b) {
                        if(a.code === b) {
                            subjectNames.push(a.englishname);
                        }
                    })
                })
                $('#subjects').text(subjectNames.join(', '));
            }

            if (sessionStorage.getItem("uni") != null) {
                var uni = sessionStorage.getItem("uni")
                $('#narrow').text(uni.split(",").join(", "))
            }

            if (sessionStorage.getItem("postcode") != null) {
                var postcode = sessionStorage.getItem("postcode")
                $('#narrow').text(postcode.split(",").join(", "))
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
