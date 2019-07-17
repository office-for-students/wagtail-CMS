from django.shortcuts import render

from courses.models import CourseDetailPage, Course


def courses_detail(request, institution_id, course_id, kis_mode):
    course, error = Course.find(institution_id, course_id, kis_mode)

    if error:
        return render(request, '500.html')

    page = CourseDetailPage.objects.get()

    context = {
        'page': page,
        'course': course,
    }

    return render(request, 'courses/course_detail_page.html', context)

