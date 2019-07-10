from CMS.test.mocks import StatusMocks
from errors.models import InternalError


def choose_country_sibling_finder(pages_list):
    def is_choose_country(sibling):
        from coursefinder.models import CourseFinderChooseCountry

        if type(sibling) == CourseFinderChooseCountry:
            return True
        else:
            return False

    choose_country_page = list(filter(is_choose_country, pages_list))

    if len(choose_country_page) == 0:
        InternalError(StatusMocks.HTTP_500_INTERNAL_SERVER_ERROR, 'Bad configuration - No country chooser page')
        return None

    if len(choose_country_page) > 1:
        InternalError(StatusMocks.HTTP_500_INTERNAL_SERVER_ERROR,
                      'Bad configuration - Found multiple country chooser pages')
    return choose_country_page[0]


def mode_of_study_sibling_finder(page):
    def is_mode_of_study(sibling):
        from coursefinder.models import CourseFinderModeOfStudy

        if type(sibling) == CourseFinderModeOfStudy:
            return True
        else:
            return False

    mode_of_study_page = list(filter(is_mode_of_study, page.get_siblings().specific()))

    if len(mode_of_study_page) == 0:
        InternalError(StatusMocks.HTTP_500_INTERNAL_SERVER_ERROR, 'Bad configuration - No mode of study pages')
        return None

    if len(mode_of_study_page) > 1:
        InternalError(StatusMocks.HTTP_500_INTERNAL_SERVER_ERROR,
                      'Bad configuration - Found multiple mode of study pages')
    return mode_of_study_page[0]


def choose_subject_sibling_finder(page):
    def is_choose_subject(sibling):
        from coursefinder.models import CourseFinderChooseSubject

        if type(sibling) == CourseFinderChooseSubject:
            return True
        else:
            return False

    choose_subject_page = list(filter(is_choose_subject, page.get_siblings().specific()))

    if len(choose_subject_page) == 0:
        InternalError(StatusMocks.HTTP_500_INTERNAL_SERVER_ERROR, 'Bad configuration - No choose subject page')
        return None

    if len(choose_subject_page) > 1:
        InternalError(StatusMocks.HTTP_500_INTERNAL_SERVER_ERROR,
                      'Bad configuration - Found multiple choose subject pages')
    return choose_subject_page[0]


def narrow_search_sibling_finder(page):
    def is_narrow_search(sibling):
        from coursefinder.models import CourseFinderNarrowSearch

        if type(sibling) == CourseFinderNarrowSearch:
            return True
        else:
            return False

    narrow_search_page = list(filter(is_narrow_search, page.get_siblings().specific()))

    if len(narrow_search_page) == 0:
        InternalError(StatusMocks.HTTP_500_INTERNAL_SERVER_ERROR, 'Bad configuration - No narrow search page')
        return None

    if len(narrow_search_page) > 1:
        InternalError(StatusMocks.HTTP_500_INTERNAL_SERVER_ERROR,
                      'Bad configuration - Found multiple narrow search pages')
    return narrow_search_page[0]


def postcode_sibling_finder(page):
    def is_postcode(sibling):
        from coursefinder.models import CourseFinderPostcode

        if type(sibling) == CourseFinderPostcode:
            return True
        else:
            return False

    postcode_page = list(filter(is_postcode, page.get_siblings().specific()))

    if len(postcode_page) == 0:
        InternalError(StatusMocks.HTTP_500_INTERNAL_SERVER_ERROR, 'Bad configuration - No postcode page')
        return None

    if len(postcode_page) > 1:
        InternalError(StatusMocks.HTTP_500_INTERNAL_SERVER_ERROR,
                      'Bad configuration - Found multiple postcode pages')
    return postcode_page[0]


def summary_sibling_finder(page):
    def is_summary(sibling):
        from coursefinder.models import CourseFinderSummary

        if type(sibling) == CourseFinderSummary:
            return True
        else:
            return False

    summary_page = list(filter(is_summary, page.get_siblings().specific()))

    if len(summary_page) == 0:
        InternalError(StatusMocks.HTTP_500_INTERNAL_SERVER_ERROR, 'Bad configuration - No summary page')
        return None

    if len(summary_page) > 1:
        InternalError(StatusMocks.HTTP_500_INTERNAL_SERVER_ERROR,
                      'Bad configuration - Found multiple summary pages')
    return summary_page[0]


def results_sibling_finder(page):
    def is_results(sibling):
        from coursefinder.models import CourseFinderResults

        if type(sibling) == CourseFinderResults:
            return True
        else:
            return False

    results_page = list(filter(is_results, page.get_siblings().specific()))

    if len(results_page) == 0:
        InternalError(StatusMocks.HTTP_500_INTERNAL_SERVER_ERROR, 'Bad configuration - No results page')
        return None

    if len(results_page) > 1:
        InternalError(StatusMocks.HTTP_500_INTERNAL_SERVER_ERROR,
                      'Bad configuration - Found multiple results pages')
    return results_page[0]
