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

                if (this.subject.value != "disabled") {
                  subject = this.subjectCode.value
                } else if (this.subjectArea.value === "disabled" && this.subject.value === "disabled") {
                  subject = ""
                } else {
                  subject = this.subjectArea.value
                }

                if (this.subjectArea.value != "disabled" && this.subject.value === "disabled") {
                  $.each(JSON.parse(sessionStorage.getItem("subjectJSON")), function(index, item) {
                    if(item.level === "3" && item.code.includes(this.subjectArea.value)) {
                      subjectCodes += item.code + ","
                    }
                  })
                } else if (this.subjectArea.value === "disabled" && this.subject.value === "disabled") {
                  subjectCodes = ""
                } else {
                  subjectCodes = this.subjectCode.value
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
