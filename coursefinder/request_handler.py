import requests
import urllib.parse
from django.conf import settings

from CMS.test.mocks.search_mocks import SearchMocks


def query_course_and_institution(course, institution, limit, offset, language):
    if settings.LOCAL:
        return SearchMocks.get_successful_search_response()
    else:
        headers = {
            'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
        }
        base_url = "%s?limit=%s&offset=%s&qc=%s&institutions=%s&language=%s"
        institution_query = urllib.parse.quote_plus(institution)
        course_query = urllib.parse.quote_plus(course)
        return requests.get(url=base_url % (settings.SEARCHAPIHOST, limit, offset, course_query, institution_query, language),
                            headers=headers)


def course_finder_query(subject, institution, countries, postcode, filters, course_query, limit, offset, language):
    if settings.LOCAL:
        return SearchMocks.get_successful_search_response()
    else:
        headers = {
            'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
        }
        url = "%s?limit=%s&offset=%s&language=%s" % (settings.SEARCHAPIHOST, limit, offset, language)
        if subject and subject != '':
            url = f"{url}&subjects={subject}"
        if course_query and course_query != '':
            encoded_course_query = urllib.parse.quote_plus(course_query)
            url = f"{url}&qc={encoded_course_query}"
        if institution and institution != '':
            encoded_institution_query = urllib.parse.quote_plus(institution)
            url = f"{url}&institutions={encoded_institution_query}"
        if countries and countries != '':
            url = f"{url}&countries={countries.lower().replace(' ', '_')}"
        if postcode and postcode != '':
            url = f"{url}&postcode={postcode}"
        if filters and filters != '':
            url = f"{url}&filters={filters}"
        return requests.get(url=url, headers=headers)
