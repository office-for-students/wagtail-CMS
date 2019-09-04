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
