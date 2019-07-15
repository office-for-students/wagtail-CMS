from django.shortcuts import render
from django.http import HttpResponseRedirect

from coursefinder.models import CourseSearch, CourseFinderSearch
from coursefinder.models import CourseFinderResults


def results(request):
    query_params = request.GET
    course_search = CourseSearch(query_params.get('subject_query', ""), query_params.get('institution_query', ""),
                                 query_params.get('page', 1), query_params.get('count', 20))
    error = course_search.execute()

    if error:
        return render(request, '500.html')

    page = CourseFinderResults.objects.get()

    context = {
        'page': page,
        'search': course_search,
        'pagination_url': 'results'
    }

    return render(request, 'coursefinder/course_finder_results.html', context)


def narrow_search(request):
    institution_query = None
    post_body = request.POST
    selection = post_body.get('radioGroup', None)
    if selection == "uni":
        return HttpResponseRedirect("/course-finder/uni")
    elif selection == "city":
        return HttpResponseRedirect("/course-finder/towncity")
    elif selection == "home":
        return HttpResponseRedirect("/course-finder/postcode")
    else:
        course_finder_search = CourseFinderSearch(post_body.get('subject_query', None),
                                                  institution_query,
                                                  post_body.get('mode_query', None),
                                                  post_body.get('countries_query', None),
                                                  post_body.get('page', 1),
                                                  post_body.get('count', 20))

        error = course_finder_search.execute()

        if error:
            return render(request, '500.html')

        page = CourseFinderResults.objects.get()

        context = {
            'page': page,
            'search': course_finder_search,
            'pagination_url': 'narrow_search'
        }

        return render(request, 'coursefinder/course_finder_results.html', context)


def course_finder_results(request):
    query_params = request.GET
    course_finder_search = CourseFinderSearch(query_params.get('subject_query', None),
                                              query_params.get('institution_query', None),
                                              query_params.get('mode_query', None),
                                              query_params.get('countries_query', None),
                                              query_params.get('page', 1),
                                              query_params.get('count', 20))
    error = course_finder_search.execute()

    if error:
        return render(request, '500.html')

    page = CourseFinderResults.objects.get()

    context = {
        'page': page,
        'search': course_finder_search,
        'pagination_url': 'course_finder_results'
    }

    return render(request, 'coursefinder/course_finder_results.html', context)
