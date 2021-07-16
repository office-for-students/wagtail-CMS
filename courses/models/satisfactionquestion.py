from .utils import fallback_to


class SatisfactionQuestion:

    def __init__(self, question_data):
        self.show_data_point = False
        if question_data:
            self.show_data_point = 'agree_or_strongly_agree' in question_data
            self.description = fallback_to(question_data.get('description'), '')
            self.agree_or_strongly_agree = fallback_to(
                question_data.get('agree_or_strongly_agree'), 0)
