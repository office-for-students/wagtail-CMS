(function ($) {

    var SubjectPicker = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    SubjectPicker.prototype = {
        setup: function() {
            this.btn = this.wrapper.find('.course-finder-content__next-button');
            this.form = this.wrapper.find('.course-finder-content__question-form');

            this.startWatchers();
        },

        startWatchers: function() {
            var that = this;
            this.btn.click(function() {
                that.form.submit();
            });

            this.form.submit(function() {
                var subject = ""
                var subjectCodes = ""
                var data = this;

                if (data.subject.value != "disabled") {
                  subject = data.subjectCode.value
                } else if (data.subjectArea.value === "disabled" && data.subject.value === "disabled") {
                  subject = ""
                } else {
                  subject = data.subjectArea.value
                }

                if (data.subjectArea.value != "disabled" && data.subject.value === "disabled") {
                  $.each(JSON.parse(localStorage.getItem("subjectsJSON")), function(index, item) {
                    if(item.level === "3" && item.code.includes(data.subjectArea.value)) {
                      subjectCodes += item.code + ","
                    }
                  })
                } else if (data.subjectArea.value === "disabled" && data.subject.value === "disabled") {
                  subjectCodes = ""
                } else {
                  subjectCodes = data.subjectCode.value
                }
                sessionStorage.setItem("subject", subject)
                sessionStorage.setItem("subjectCodes", subjectCodes)
            });
        }
    }

    function init() {
        var subjectPickers = $('.subject-chooser');
        new SubjectPicker(subjectPickers[0]);
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
