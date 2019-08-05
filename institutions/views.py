from django.shortcuts import render

from CMS.enums import enums
from CMS.utils import get_page_for_language
from institutions.models import InstitutionDetailPage, Institution


def institution_detail(request, institution_id, language=enums.languages.ENGLISH):
    institution, error = Institution.find(institution_id, language)

    if error:
        return render(request, '500.html')

    page = get_page_for_language(language, InstitutionDetailPage.objects.all())

    if not page:
        return render(request, '404.html')

    page.tef_report_link = page.tef_report_link.replace('{{institution_name}}', institution.pub_ukprn_name)

    context = {
        'page': page,
        'institution': institution,
    }

    return render(request, 'institutions/institution_detail_page.html', context)
