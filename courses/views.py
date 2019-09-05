from django.shortcuts import render

from CMS.enums import enums
from core.utils import get_page_for_language

from courses.models import CourseDetailPage, Course, CourseComparisonPage


def courses_detail(request, institution_id, course_id, kis_mode, language=enums.languages.ENGLISH):
    course, error = Course.find(institution_id, course_id, kis_mode, language)

    if error:
        return render(request, '500.html')

    page = get_page_for_language(language, CourseDetailPage.objects.all())

    comparison_page = get_page_for_language(language, CourseComparisonPage.objects.all())

    if not page:
        return render(request, '404.html')

    context = {
        'page': page,
        'course': course,
        'comparison_link': comparison_page.url if comparison_page else '#'
    }

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
        return render(request, '500.html')

    if not page:
        return render(request, '404.html')

    context = {
        'page': page,
        'course1': course1,
        'course2': course2,
    }

    return render(request, 'courses/course_comparison_page.html', context)
