class Languages:
    ENGLISH = "en"
    WELSH = "cy"


class LanguagesFull:
    ENGLISH = "english"
    WELSH = "welsh"


class UniLinkKeys:
    ASSESSMENT = 'assessment_method'
    COURSE = 'course_page'
    FINANCIAL_SUPPORT = 'financial_support_details'
    TEACHING_METHODS = 'learning_and_teaching_methods'
    ACCOMMODATION = 'accommodation'
    COSTS = 'costs'
    EMPLOYMENT = 'employment_details'


class Enums:
    languages = Languages()
    languages_full = LanguagesFull()
    languages_map = {
        Languages.ENGLISH: LanguagesFull.ENGLISH,
        Languages.WELSH: LanguagesFull.WELSH
    }
    uni_link_keys = UniLinkKeys()


enums = Enums()
