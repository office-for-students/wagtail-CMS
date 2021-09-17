from CMS.enums import enums


class CourseSubject:
    def __init__(self, data_obj, language):
        self.display_language = language
        self.subject_english = data_obj.get('english', '')
        self.subject_welsh = data_obj.get('welsh', '')

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english
