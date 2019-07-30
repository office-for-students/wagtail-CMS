from django.shortcuts import render

from institutions.models import InstitutionDetailPage, Institution


def institution_detail(request, institution_id):
    institution, error = Institution.find(institution_id)

    if error:
        return render(request, '500.html')

    page = InstitutionDetailPage.objects.get()

    page.tef_report_link = page.tef_report_link.replace('{{institution_name}}', institution.pub_ukprn_name)
    print(page.tef_report_link.replace('{{institution_name}}', institution.pub_ukprn_name))

    context = {
        'page': page,
        'institution': institution,
    }

    return render(request, 'institutions/institution_detail_page.html', context)
