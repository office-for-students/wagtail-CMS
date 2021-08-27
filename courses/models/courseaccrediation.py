from .utils import enums, fallback_to


class CourseAccreditation:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.type = fallback_to(data_obj.get("type"), '')
        self.accreditor_url = fallback_to(data_obj.get('accreditor_url'), '')

        if str(self.accreditor_url)[:4] != "http":
            self.accreditor_url = 'http://' + self.accreditor_url

        text = data_obj.get('text')
        if text:
            self.text_english = fallback_to(text.get('english'), '')
            self.text_welsh = fallback_to(text.get('welsh'), '')

        url = data_obj.get('url')
        self.url_english = ''
        self.url_welsh = ''
        if url:
            self.url_english = fallback_to(url.get('english'), '')
            self.url_welsh = fallback_to(url.get('welsh'), '')

        dependent = data_obj.get('dependent_on')
        if dependent:
            self.dependent_on_code = dependent.get('code')
            self.dependent_on_label = fallback_to(dependent.get('label'), '')

    def display_text(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.text_english if self.text_english else self.text_welsh
        return self.text_welsh if self.text_welsh else self.text_english

    def language_url(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.url_english if self.url_english else self.url_welsh
        return self.url_welsh if self.url_welsh else self.url_english

    def show_dependency(self):
        return self.dependent_on_code == '1'
