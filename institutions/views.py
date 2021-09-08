from django.shortcuts import render, redirect

from CMS.enums import enums
from core.utils import get_page_for_language, get_new_landing_page_for_language
from institutions.models import InstitutionDetailPage, Institution
from site_search.models import SearchLandingPage


def institution_detail(request, institution_id, language=enums.languages.ENGLISH):
    institution, error = Institution.find(institution_id, language)

    if error:
        redirect_page = get_new_landing_page_for_language(language)
        #redirect_page = get_page_for_language(language, SearchLandingPage.objects.all()).url
        return redirect(redirect_page + '?load_error=true&error_type=0')

    page = get_page_for_language(language, InstitutionDetailPage.objects.all())

    if not page:
        return render(request, '404.html')

    page.tef_report_link = page.tef_report_link.replace('{{institution_name}}', institution.pub_ukprn_name)

    full_path = '%s?%s' % (request.path, request.environ.get('QUERY_STRING'))
    if language == enums.languages.ENGLISH:
        translated_url = '/cy' + request.path if language == enums.languages.ENGLISH else request.path
    else:
        translated_url = request.path.replace('/cy/', '/')

    context = page.get_context(request)
    context.update({
        'page': page,
        'institution': institution,
        'translated_url': translated_url,
        'cookies_accepted': request.COOKIES.get('discoverUniCookies')
    })

    return render(request, 'institutions/institution_detail_page.html', context)
