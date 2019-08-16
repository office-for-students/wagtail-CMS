from django.shortcuts import render
from django.http import HttpResponseRedirect

from CMS.enums import enums
from core.utils import get_page_for_language
from coursefinder.models import CourseSearch, CourseFinderSearch, CourseFinderUni, CourseFinderPostcode
from coursefinder.models import CourseFinderResults


def results(request, language=enums.languages.ENGLISH):
    query_params = request.GET
    course_search = CourseSearch(query_params.get('subject_query', ""), query_params.get('institution_query', ""),
                                 query_params.get('page', 1), query_params.get('count', 20))
    error = course_search.execute()

    if error:
        return render(request, '500.html')

    page = get_page_for_language(language, CourseFinderResults.objects.all())

    if not page:
        return render(request, '404.html')

    context = {
        'page': page,
        'search': course_search,
        'pagination_url': 'results'
    }

    return render(request, 'coursefinder/course_finder_results.html', context)


def narrow_search(request, language=enums.languages.ENGLISH):
    institution_query = None
    postcode_query = None
    post_body = request.POST
    page = None
    selection = post_body.get('radioGroup', None)
    if selection == "uni":
        page = get_page_for_language(language, CourseFinderUni.objects.all())
    elif selection == "home":
        page = get_page_for_language(language, CourseFinderPostcode.objects.all())
    elif selection == 'all':
        course_finder_search = CourseFinderSearch(post_body.get('subject_query', None),
                                                  institution_query,
                                                  post_body.get('mode_query', None),
                                                  post_body.get('countries_query', None),
                                                  postcode_query,
                                                  post_body.get('page', 1),
                                                  post_body.get('count', 20))

        error = course_finder_search.execute()

        if error:
            return render(request, '500.html')

        page = get_page_for_language(language, CourseFinderResults.objects.all())

        if page:
            context = {
                'page': page,
                'search': course_finder_search,
                'pagination_url': 'narrow_search'
            }

            return render(request, 'coursefinder/course_finder_results.html', context)

    if page:
        return HttpResponseRedirect(page.url)
    return render(request, '404.html')


def course_finder_results(request, language=enums.languages.ENGLISH):
    query_params = request.GET
    course_finder_search = CourseFinderSearch(query_params.get('subject_query', None),
                                              query_params.get('institution_query', None),
                                              query_params.get('mode_query', None),
                                              query_params.get('countries_query', None),
                                              query_params.get('postcode_query', None),
                                              query_params.get('page', 1),
                                              query_params.get('count', 20))
    error = course_finder_search.execute()

    if error:
        return render(request, '500.html')

    page = get_page_for_language(language, CourseFinderResults.objects.all())

    if not page:
        return render(request, '404.html')

    context = {
        'page': page,
        'search': course_finder_search,
        'pagination_url': 'course_finder_results'
    }

    return render(request, 'coursefinder/course_finder_results.html', context)
