(function ($) {

    var FeedbackForm = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    FeedbackForm.prototype = {
        setup: function() {
            this.yesButton = this.wrapper.find('#yes');
            this.noButton = this.wrapper.find('#no');
            this.formHeading = this.wrapper.find('.feedback-form__heading');
            this.formBody = this.wrapper.find('.feedback-form__body');
            this.errorMessage = this.wrapper.find('.feedback-form__error-message');
            this.form = this.wrapper.find('.feedback-form__form');
            this.usefulField = this.wrapper.find('#useful');
            this.improvementField = this.wrapper.find('#improvement');
            this.closeBtn = this.wrapper.find('#close');
            this.submitBtn = this.wrapper.find('.feedback-form__submit-button');

            this.startWatchers();
        },

        startWatchers: function() {
            var that = this;
            this.yesButton.click(function() {
                that.formHeading.hide();
                that.formBody.show();
                that.improvementField.hide();
            });

            this.noButton.click(function() {
                that.formHeading.hide();
                that.formBody.show();
                that.usefulField.hide();
            });

            this.closeBtn.click(function() {
                that.handleFormClose();
            })

            this.submitBtn.click(function() {
                var formData = that.form.serializeArray();
                data = {
                    "page": window.location.href,
                }
                
                for (var i = 0; i < formData.length; i++) {
                    data[formData[i].name] = formData[i].value;
                }

                var url = window.location.origin + '/feedback';
                $.post(url, data, function(data,status,xhr) {
                    that.handleSubmissionSuccess();
                }, 'json')
                .fail(function(data,status,xhr) {
                    that.handleSubmissionError();
                });
            })
        },

        handleFormClose: function() {
            this.formHeading.show();
            this.usefulField.show();
            this.improvementField.show();
            this.formBody.hide();
            this.form[0].reset();
        },

        handleSubmissionSuccess: function() {
            this.errorMessage.hide();
            this.handleFormClose();
        },

        handleSubmissionError: function() {
            this.errorMessage.show();
        }
    }

    function init() {
        var feedbackForm = $('.feedback-form__wrapper');
        for (var i = 0; i < feedbackForm.length; i++) {
            new FeedbackForm(feedbackForm[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
