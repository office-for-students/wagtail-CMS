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
                    "page": window.location,
                    "questions": []
                }
                
                for (var i = 0; i < formData.length; i++) {
                    if (formData[i].name === 'helpful') {
                        data['is_useful'] = formData[i].value === 'yes';
                    }
                    else {
                        data.questions.push({
                            'title': formData[i].name,
                            'feedback': formData[i].value
                        });
                    }
                }

                $.post(that.form[0].dataset.api, JSON.stringify(data), function() {
                    that.handleSubmissionSuccess();
                })
                .fail(function() {
                    that.handleSubmissionError();
                });
            })
        },

        handleFormClose: function() {
            that.formHeading.show();
            that.usefulField.show();
            that.improvementField.show();
            that.formBody.hide();
            that.form[0].reset();
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
