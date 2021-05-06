from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from CMS.enums import enums
from core.utils import get_page_for_language, get_new_landing_page_for_language
from coursefinder.forms import FilterForm
from coursefinder.models import CourseSearch, CourseFinderSearch, CourseFinderUni, CourseFinderPostcode, \
    CourseFinderSummary
from coursefinder.models import CourseFinderResults
from courses.models import CourseComparisonPage, CourseManagePage
from site_search.models import SearchLandingPage
from home.models import HomePage

import json

def results(request, language=enums.languages.ENGLISH):
    query_params = request.POST
    search_form = FilterForm({
        "course_query" : query_params.get('subject_query', ""),
        "institution_query": query_params.get('institution_query', ""),
    })

    course_search = CourseSearch(query_params.get('subject_query', ""),
                                 query_params.get('institution_query', ""),
                                 query_params.get('page', 1),
                                 query_params.get('count', 20),
                                 language)
    error = course_search.execute()

    if error:
        redirect_page = get_new_landing_page_for_language(language)
        #redirect_page = get_page_for_language(language, SearchLandingPage.objects.all()).url
        return redirect(redirect_page + '?load_error=true&error_type=1')

    page = get_page_for_language(language, CourseFinderResults.objects.all())

    if not page:
        return render(request, '404.html')

    comparison_page = get_page_for_language(language, CourseComparisonPage.objects.all())
    bookmark_page = get_page_for_language(language, CourseManagePage.objects.all())

    full_path = '%s?%s' % (request.path, request.environ.get('QUERY_STRING'))
    welsh_url = '/cy' + full_path if language == enums.languages.ENGLISH else full_path
    english_url = full_path.replace('/cy/', '/')

    context = page.get_context(request)
    context.update({
        'page': page,
        'search': course_search,
        'pagination_url': 'results',
        'comparison_link': comparison_page.url if comparison_page else '#',
        'manage_link': bookmark_page.url if bookmark_page else '#',
        'english_url': english_url,
        'welsh_url': welsh_url,
        'cookies_accepted': request.COOKIES.get('discoverUniCookies'),
        'filter_form': search_form
    })

    return render(request, 'coursefinder/course_finder_results.html', context)


def narrow_search(request, language=enums.languages.ENGLISH):
    post_body = request.POST
    selection = post_body.get('radioGroup', None)
    if selection == "uni":
        page = get_page_for_language(language, CourseFinderUni.objects.all())
    elif selection == "home":
        page = get_page_for_language(language, CourseFinderPostcode.objects.all())
    else:
        page = get_page_for_language(language, CourseFinderSummary.objects.all())

    if page:
        return HttpResponseRedirect(page.url)
    return render(request, '404.html')

    
def course_finder_results(request, language=enums.languages.ENGLISH):
    query_params = request.POST
    countries_query = ','.join(query_params.getlist('countries_query')) if 'countries_query' in query_params else None
    filter_form = FilterForm(query_params)
    filters = build_filters(query_params)
    course_finder_search = CourseFinderSearch(query_params.get('subject_query', None),
                                              query_params.get('institution_query', None),
                                              countries_query,
                                              query_params.get('postcode_query', None),
                                              filters,
                                              query_params.get('course_query', None),
                                              query_params.get('page', 1),
                                              query_params.get('count', 20),
                                              language)
    error = course_finder_search.execute()
 
    if error:
        redirect_page = get_new_landing_page_for_language(language)
        #redirect_page = get_page_for_language(language, SearchLandingPage.objects.all()).url

        return redirect(redirect_page + '?load_error=true&error_type=1')

    page = get_page_for_language(language, CourseFinderResults.objects.all())

    comparison_page = get_page_for_language(language, CourseComparisonPage.objects.all())
    bookmark_page = get_page_for_language(language, CourseManagePage.objects.all())

    welsh_url = '/cy' + request.path if language == enums.languages.ENGLISH else request.path
    english_url = request.path.replace('/cy/', '/')

    if not page:
        return render(request, '404.html')

    context = page.get_context(request)

    context.update({
        'page': page,
        'search': course_finder_search,
        'pagination_url': 'course_finder_results',
        'comparison_link': comparison_page.url if comparison_page else '#',
        'manage_link': bookmark_page.url if bookmark_page else '#',
        'english_url': english_url,
        'welsh_url': welsh_url,
        'cookies_accepted': request.COOKIES.get('discoverUniCookies'),
        'filter_form': filter_form
    })

    return render(request, 'coursefinder/course_finder_results.html', context)


def build_filters(params):
    filters = []

    if 'mode_query' in params:
        mode_query = ','.join(params.getlist('mode_query'))
        if 'Full-time,Part-time' not in mode_query:
            filters.append(params.get('mode_query').lower().replace('-', '_').replace(' ', '_'))
    if 'qualification_query' in params:
        qualification_query = ','.join(params.getlist('qualification_query'))
        if 'first_degree,other_undergraduate' not in qualification_query:
            filters.append(params.get('qualification_query'))
    if 'placement' in params:
        if params.get('placement') == 'yes':
            filters.append('sandwich_year')
        elif params.get('placement') == 'no':
            filters.append('-sandwich_year')
    if 'foundation' in params:
        if params.get('foundation') == 'yes':
            filters.append('foundation_year')
        elif params.get('foundation') == 'no':
            filters.append('-foundation_year')
    if 'abroad' in params:
        if params.get('abroad') == 'yes':
            filters.append('year_abroad')
        elif params.get('abroad') == 'no':
            filters.append('-year_abroad')

    filters_query_params = ','.join(filter_ for filter_ in filters if filter_)
    return filters_query_params
