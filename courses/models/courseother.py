from .utils import enums, fallback_to, DICT


class CourseDistanceLearning:

    def __init__(self, data_obj, language):
        self.display_language = language
        if data_obj:
            self.code = str(data_obj.get('code'))
            self.label = fallback_to(data_obj.get('label'), '')

    def display_label(self):
        if self.code is not None and self.code in DICT.get('distance_learning_values'):
            return DICT.get('distance_learning_values').get(self.code).get(self.display_language)
        return DICT.get('unknown').get(self.display_language)


class CourseFoundationYear:

    def __init__(self, data_obj, language):
        self.label = DICT.get('unknown').get(language)
        if data_obj:
            self.code = data_obj.get('code')
            self.label = fallback_to(data_obj.get('label'), '')


class CourseLength:

    def __init__(self, data_obj, language):
        self.label = 0
        if data_obj:
            self.code = data_obj.get('code')
            self.label = fallback_to(data_obj.get('label'), '')


class CourseLink:

    def __init__(self, name, link_obj, language_key):
        self.label = name
        if language_key in link_obj:
            self.link = link_obj.get(language_key)
        else:
            self.link = fallback_to(link_obj.get(enums.languages_full.ENGLISH), '')


class CourseLocation:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.latitude = data_obj.get('latitude')
        self.longitude = data_obj.get('longitude')
        name = data_obj.get('name')
        if name:
            self.english_name = fallback_to(name.get('english'), '')
            self.welsh_name = fallback_to(name.get('welsh'), '')
        self.links = data_obj.get('links')

    def display_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.english_name if self.english_name else self.welsh_name
        else:
            return self.welsh_name if self.welsh_name else self.english_name
