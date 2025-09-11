class SatisfactionQuestion:

    def __init__(self, question_data):
        self.show_data_point = False
        self.description = ''
        self.agree_or_strongly_agree = ''
        if question_data:
            self.show_data_point = 'agree_or_strongly_agree' in question_data
            self.description = question_data.get('description', '')
            self.agree_or_strongly_agree = question_data.get('agree_or_strongly_agree')


    def __str__(self):
        if self.show_data_point:
            return str(self.agree_or_strongly_agree)