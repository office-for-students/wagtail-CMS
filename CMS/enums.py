class Languages:
    ENGLISH = "en"
    WELSH = "cy"


class LanguagesFull:
    ENGLISH = "english"
    WELSH = "welsh"


class Countries:
    ENGLAND = 'XF'
    WALES = 'XI'
    SCOTLAND = 'XH'
    IRELAND = 'XG'


class APRValues:
    MET = 'Meets requirements'
    ACTION_PLAN = 'Meets requirements with an action plan'
    PENDING = 'Pending'
    NOT_MET = 'Does not meet requirements'


class TEFValues:
    GOLD = 'Gold'
    SILVER = 'Silver'
    BRONZE = 'Bronze'
    PROVISIONAL = 'Provisional'
    NOT_PARTICIPATE = 'Did not participate'
    WITHDRAWN = 'Withdrawn'


class UniLinkKeys:
    ASSESSMENT = 'assessment_method'
    COURSE = 'course_page'
    FINANCIAL_SUPPORT = 'financial_support_details'
    TEACHING_METHODS = 'learning_and_teaching_methods'
    ACCOMMODATION = 'accommodation'
    COSTS = 'course_cost'
    EMPLOYMENT = 'employment_details'


class CahCodeLevels:
    ONE = 1
    TWO = 2
    THREE = 3


class Enums:
    languages = Languages()
    languages_full = LanguagesFull()
    languages_map = {
        Languages.ENGLISH: LanguagesFull.ENGLISH,
        Languages.WELSH: LanguagesFull.WELSH
    }
    countries = Countries()
    apr_values = APRValues()
    tef_values = TEFValues()
    uni_link_keys = UniLinkKeys()
    cah_code_levels = CahCodeLevels()


enums = Enums()
