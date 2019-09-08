from django.shortcuts import render

from CMS.enums import enums
from core.utils import get_page_for_language
from institutions.models import InstitutionDetailPage, Institution


def institution_detail(request, institution_id, language=enums.languages.ENGLISH):
    institution, error = Institution.find(institution_id, language)

    if error:
        return render(request, '500.html')

    page = get_page_for_language(language, InstitutionDetailPage.objects.all())

    if not page:
        return render(request, '404.html')

    page.tef_report_link = page.tef_report_link.replace('{{institution_name}}', institution.pub_ukprn_name)

    full_path = '%s?%s' % (request.path, request.environ.get('QUERY_STRING'))
    welsh_url = '/cy' + full_path if language == enums.languages.ENGLISH else full_path
    english_url = full_path.replace('/cy/', '/')

    context = {
        'page': page,
        'institution': institution,
        'english_url': english_url,
        'welsh_url': welsh_url,
        'cookies_accepted': request.COOKIES['discoverUniCookies']
    }

    return render(request, 'institutions/institution_detail_page.html', context)
