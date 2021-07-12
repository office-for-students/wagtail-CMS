from django.conf import settings
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
import os

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
    filter_form = FilterForm(query_params)
    filters = build_filters(query_params)
    if "distance" in filters and "campus" not in filters:
        countries_query = ''
    else: 
        countries_query = ','.join(query_params.getlist('countries_query')) if 'countries_query' in query_params else None

    institution_query = '@'.join(query_params.getlist('institution_query')) if 'institution_query' in query_params else None
    
    postcode = query_params.get('postcode') if 'postcode' in query_params else None
    distance_query = query_params.get('distance') if 'distance' in query_params else None
    postcode_query = (postcode + ',' + distance_query) if postcode and distance_query else {}

    sort_by_subject_enabled = query_params.get('sort_by_subject', 'false')
    sort_by_subject_limit = int(os.environ.get('SORT_BY_SUBJECT_LIMIT', 5000))
    count = sort_by_subject_limit if sort_by_subject_enabled == 'true' else 20

    course_finder_search = CourseFinderSearch(query_params.get('subject_query', None),
                                              institution_query,
                                              countries_query,
                                              postcode_query,
                                              filters,
                                              sort_by_subject_enabled,
                                              sort_by_subject_limit,
                                              query_params.get('course_query', None),
                                              query_params.get('page', 1),
                                              count,
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
        'filter_form': filter_form,
        'filters': filters,
        'postcode_query': postcode_query,
        'sort_by_subject_enabled': sort_by_subject_enabled,
        'sort_by_subject_limit': sort_by_subject_limit,  
    })

    return render(request, 'coursefinder/course_finder_results.html', context)


def build_study_mode_filter(list):
    filter = ''
    if (len(list) > 1 and list[0:2] == ['Full-time', 'Part-time']):
        filter = ','.join(list[2:])
    else:
        filter = ','.join(list)
    return transform_study_mode_filter_name(filter)


def transform_study_mode_filter_name(filter):
    return filter.lower().replace('-', '_').replace(' ', '_')


def build_filters(params):
    filters = []

    if 'mode_query' in params:
        mode_query = params.getlist('mode_query')
        filters.append(build_study_mode_filter(mode_query))
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
        