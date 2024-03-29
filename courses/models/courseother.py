from CMS.enums import enums
from CMS.translations import term_for_key
from CMS.translations.dictionaries.general import DICT


class CourseDistanceLearning:

    def __init__(self, data_obj, language):
        self.display_language = language
        if data_obj:
            self.code = str(data_obj.get('code'))
            self.label = data_obj.get('label', '')

    def display_label(self):
        if self.code is not None and self.code in DICT.get('distance_learning_values'):
            return DICT.get('distance_learning_values').get(self.code).get(self.display_language)
        return DICT.get('unknown').get(self.display_language)


class CourseFoundationYear:

    def __init__(self, data_obj, language):
        self.label = term_for_key(key='unknown', language=language)
        if data_obj:
            self.code = data_obj.get('code')
            self.label = data_obj.get('label', '')


class CourseLength:

    def __init__(self, data_obj, language):
        self.label = 0
        if data_obj:
            self.code = data_obj.get('code')
            self.label = data_obj.get('label', '')


class CourseLink:

    def __init__(self, name, link_obj, language_key):
        self.label = name
        if language_key in link_obj:
            self.link = link_obj.get(language_key)
        else:
            self.link = link_obj.get(enums.languages_full.ENGLISH, '')


class CourseLocation:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.latitude = data_obj.get('latitude')
        self.longitude = data_obj.get('longitude')
        name = data_obj.get('name')
        if name:
            self.english_name = name.get('english', '')
            self.welsh_name = name.get('welsh', '')
        else:
            self.english_name = ''
            self.welsh_name = ''
        self.links = data_obj.get('links')

    def display_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.english_name if self.english_name else self.welsh_name
        else:
            return self.welsh_name if self.welsh_name else self.english_name
