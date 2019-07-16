from django.shortcuts import render

from courses.models import CourseDetailPage


def courses_detail(request, institution_id, course_id, kis_mode):
    course = Course.find(institution_id, course_id, kis_mode)

    page = CourseDetailPage.objects.get()

    context = {
        'page': page,
    }

    return render(request, 'courses/course_detail_page.html', context)

