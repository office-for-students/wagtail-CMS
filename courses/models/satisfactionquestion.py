class SatisfactionQuestion:

    def __init__(self, question_data, question_number):
        self.show_data_point = False
        if type(question_data) is int:
            # self.show_data_point = 'agree_or_strongly_agree' in question_data
            # self.description = question_data.get('description', '')
            self.show_data_point = True
            self.description = question_number
            self.agree_or_strongly_agree = question_data

    def __str__(self):
        if self.show_data_point:
            # return str(self.agree_or_strongly_agree)
            return True
        return False
