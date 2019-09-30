(function ($) {

    var FeedbackForm = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    FeedbackForm.prototype = {
        setup: function() {
            this.toggleBtn = this.wrapper.find('.feedback-form__toggle');
            this.formHeading = this.wrapper.find('.feedback-form__message');
            this.feedbackThankYou = this.wrapper.find('.feed-form__thank-you');
            this.formBody = this.wrapper.find('.feedback-form__body');
            this.errorMessage = this.wrapper.find('.feedback-form__error-message');
            this.form = this.wrapper.find('.feedback-form__form');
            this.submitBtn = this.wrapper.find('.feedback-form__submit-button');

            this.startWatchers();
        },

        startWatchers: function() {
            var that = this;
            this.toggleBtn.click(function() {
                that.formBody.show();
            });

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
