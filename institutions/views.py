from django.shortcuts import render

from institutions.models import InstitutionDetailPage


def institution_detail(request, institution_id):
    institution, error = Institution.find(institution_id)

    if error:
        return render(request, '500.html')

    page = InstitutionDetailPage.objects.get()

    context = {
        'page': page,
        'institution': institution,
    }

    return render(request, 'courses/course_detail_page.html', context)

