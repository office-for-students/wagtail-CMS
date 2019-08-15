import requests
from django.conf import settings

from CMS.test.mocks import SearchMocks


def query_course_and_institution(course, institution, limit, offset):
    if settings.LOCAL:
        return SearchMocks.get_successful_search_response()
    else:
        headers = {
            'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
        }
        base_url = "%s?limit=%s&offset=%s&qc=%s&qi=%s"
        return requests.get(url=base_url % (settings.SEARCHAPIHOST, limit, offset, course, institution),
                            headers=headers)


def course_finder_query(subject, institution, mode, countries, limit, offset):
    if settings.LOCAL:
        return SearchMocks.get_successful_search_response()
    else:
        headers = {
            'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
        }
        url = "%s?limit=%s&offset=%s" % (settings.SEARCHAPIHOST, limit, offset)
        if subject and subject != '':
            url = f"{url}&qc={subject}"
        if institution and institution != '':
            url = f"{url}&qi={institution}"
        if mode and 'Full-time,Part-time' not in mode and mode != '':
            url = f"{url}&filters={mode.lower().replace('-', '_').replace(' ', '_')}"
        if countries and countries != '':
            url = f"{url}&countries={countries.lower().replace(' ', '_')}"
        return requests.get(url=url, headers=headers)
