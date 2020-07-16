from django.shortcuts import render, redirect

from CMS.enums import enums
from core.utils import get_page_for_language

from courses.models import CourseDetailPage, Course, CourseComparisonPage, CourseManagePage
from site_search.models import SearchLandingPage

# apw added.
from django.http import JsonResponse
# from django.urls import reverse
# from azure.cosmos import CosmosClient, PartitionKey, exceptions
# import os
# import json


def refresh_dummy_field(request):
    if 'region' in request.POST and request.is_ajax():
        # TODO: call query_cosmos_db_directly()
        x = request.POST['region']
        resp = { 'updated_dummy_field_val': 'HTML Element for Ajax Refresh: views.py says: ' + x }
        # course, error = Course.find(institution_id, course_id, kis_mode, language)
        return JsonResponse(resp)
    else:
        return JsonResponse({'retval': 'apw error'}),
# apw added.


def courses_detail(request, institution_id, course_id, kis_mode, language=enums.languages.ENGLISH):
    course, error = Course.find(institution_id, course_id, kis_mode, language)

    if error:
        redirect_page = get_page_for_language(language, SearchLandingPage.objects.all()).url
        return redirect(redirect_page + '?load_error=true&error_type=0')

    page = get_page_for_language(language, CourseDetailPage.objects.all())

    page.uni_site_links_header = page.uni_site_links_header.replace('{{institution_name}}',
                                                                    course.institution.pub_ukprn_name)

    comparison_page = get_page_for_language(language, CourseComparisonPage.objects.all())
    bookmark_page = get_page_for_language(language, CourseManagePage.objects.all())

    if not page:
        return render(request, '404.html')

    full_path = '%s?%s' % (request.path, request.environ.get('QUERY_STRING'))
    welsh_url = '/cy' + full_path if language == enums.languages.ENGLISH else full_path
    english_url = full_path.replace('/cy/', '/')

    context = page.get_context(request)
    context.update({
        'page': page,
        'course': course,
        'comparison_link': comparison_page.url if comparison_page else '#',
        'manage_link': bookmark_page.url if bookmark_page else '#',
        'english_url': english_url,
        'welsh_url': welsh_url,
        'cookies_accepted': request.COOKIES.get('discoverUniCookies')
    })

    return render(request, 'courses/course_detail_page.html', context)


def compare_courses(request, language=enums.languages.ENGLISH):
    get_params = request.GET
    error1 = None
    error2 = None
    course1 = None
    course2 = None

    course1_params = get_params.get('course1').split(',') if 'course1' in get_params else None
    course2_params = get_params.get('course2').split(',') if 'course2' in get_params else None

    page = get_page_for_language(language, CourseComparisonPage.objects.all())

    if course1_params:
        course1, error1 = Course.find(course1_params[0], course1_params[1], course1_params[2], language)
    if course2_params:
        course2, error2 = Course.find(course2_params[0], course2_params[1], course2_params[2], language)

    if error1 or error2:
        redirect_page = get_page_for_language(language, SearchLandingPage.objects.all()).url
        return redirect(redirect_page + '?load_error=true&error_type=0')

    if not page:
        return render(request, '404.html')

    query_string = request.environ.get('QUERY_STRING')
    english_url = page.get_english_url() + query_string
    welsh_url = page.get_welsh_url() + query_string

    context = page.get_context(request)
    context.update({
        'page': page,
        'course1': course1,
        'course2': course2,
        'english_url': english_url,
        'welsh_url': welsh_url,
        'cookies_accepted': request.COOKIES.get('discoverUniCookies')
    })

    return render(request, 'courses/course_comparison_page.html', context)
