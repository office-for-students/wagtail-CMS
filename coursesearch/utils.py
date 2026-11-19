from http import HTTPStatus

from errors.models import InternalError


def choose_country_sibling_finder(pages_list):
    def is_choose_country(sibling):
        from coursesearch.models import CourseFinderChooseCountry

        return type(sibling) is CourseFinderChooseCountry

    choose_country_page = list(filter(is_choose_country, pages_list))

    if not choose_country_page:
        InternalError(HTTPStatus.INTERNAL_SERVER_ERROR, 'Bad configuration - No country chooser page')
        return None

    if len(choose_country_page) > 1:
        InternalError(HTTPStatus.INTERNAL_SERVER_ERROR, 'Bad configuration - Found multiple country chooser pages')
    return choose_country_page[0]


def mode_of_study_sibling_finder(page):
    def is_mode_of_study(sibling):
        from coursesearch.models import CourseFinderModeOfStudy

        return type(sibling) is CourseFinderModeOfStudy

    mode_of_study_page = list(filter(is_mode_of_study, page.get_siblings().specific()))

    if not mode_of_study_page:
        InternalError(HTTPStatus.INTERNAL_SERVER_ERROR, 'Bad configuration - No mode of study pages')
        return None

    if len(mode_of_study_page) > 1:
        InternalError(HTTPStatus.INTERNAL_SERVER_ERROR, 'Bad configuration - Found multiple mode of study pages')
    return mode_of_study_page[0]


def choose_subject_sibling_finder(page):
    def is_choose_subject(sibling):
        from coursesearch.models import CourseFinderChooseSubject

        return type(sibling) is CourseFinderChooseSubject

    choose_subject_page = list(filter(is_choose_subject, page.get_siblings().specific()))

    if not choose_subject_page:
        InternalError(HTTPStatus.INTERNAL_SERVER_ERROR, 'Bad configuration - No choose subject page')
        return None

    if len(choose_subject_page) > 1:
        InternalError(HTTPStatus.INTERNAL_SERVER_ERROR, 'Bad configuration - Found multiple choose subject pages')
    return choose_subject_page[0]


def narrow_search_sibling_finder(page):
    def is_narrow_search(sibling):
        from coursesearch.models import CourseFinderNarrowSearch

        return type(sibling) is CourseFinderNarrowSearch

    narrow_search_page = list(filter(is_narrow_search, page.get_siblings().specific()))

    if not narrow_search_page:
        InternalError(HTTPStatus.INTERNAL_SERVER_ERROR, 'Bad configuration - No narrow search page')
        return None

    if len(narrow_search_page) > 1:
        InternalError(HTTPStatus.INTERNAL_SERVER_ERROR, 'Bad configuration - Found multiple narrow search pages')
    return narrow_search_page[0]


def postcode_sibling_finder(page):
    def is_postcode(sibling):
        from coursesearch.models import CourseFinderPostcode

        return type(sibling) is CourseFinderPostcode

    postcode_page = list(filter(is_postcode, page.get_siblings().specific()))

    if not postcode_page:
        InternalError(HTTPStatus.INTERNAL_SERVER_ERROR, 'Bad configuration - No postcode page')
        return None

    if len(postcode_page) > 1:
        InternalError(HTTPStatus.INTERNAL_SERVER_ERROR, 'Bad configuration - Found multiple postcode pages')
    return postcode_page[0]


def summary_sibling_finder(page):
    def is_summary(sibling):
        from coursesearch.models import CourseFinderSummary

        return type(sibling) is CourseFinderSummary

    summary_page = list(filter(is_summary, page.get_siblings().specific()))

    if not summary_page:
        InternalError(HTTPStatus.INTERNAL_SERVER_ERROR, 'Bad configuration - No summary page')
        return None

    if len(summary_page) > 1:
        InternalError(HTTPStatus.INTERNAL_SERVER_ERROR, 'Bad configuration - Found multiple summary pages')
    return summary_page[0]


def results_sibling_finder(page):
    def is_results(sibling):
        from coursesearch.models import CourseFinderResults

        return type(sibling) is CourseFinderResults

    results_page = list(filter(is_results, page.get_siblings().specific()))

    if not results_page:
        InternalError(HTTPStatus.INTERNAL_SERVER_ERROR, 'Bad configuration - No results page')
        return None

    if len(results_page) > 1:
        InternalError(HTTPStatus.INTERNAL_SERVER_ERROR, 'Bad configuration - Found multiple results pages')
    return results_page[0]
