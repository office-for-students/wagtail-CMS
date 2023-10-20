import json
import urllib

import requests
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
        return requests.get(
            url=base_url % (settings.SEARCHAPIHOST, limit, offset, course_query, institution_query, language),
            headers=headers)


def course_finder_query(subject,
                        institution,
                        countries,
                        postcode,
                        filters,
                        sortBySubject,
                        sortBySubjectLimit,
                        course_query,
                        limit,
                        offset,
                        language):
    institution_dict = {}

    if settings.LOCAL:
        return SearchMocks.get_successful_search_response()
    else:
        headers = {
            'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY,
            'Content-Type': 'application/json'
        }
        url = "%s?limit=%s&offset=%s&language=%s" % (settings.SEARCHAPIHOST, limit, offset, language)
        if subject and subject != '':
            url = f"{url}&subjects={subject}"
        if course_query and course_query != '':
            encoded_course_query = urllib.parse.quote_plus(course_query)
            url = f"{url}&qc={encoded_course_query}"
        if institution and institution != '':
            institution_list = institution.split("@")
            institution_dict = dict(institutions=institution_list)
        if countries and countries != '':
            url = f"{url}&countries={countries.lower().replace(' ', '_')}"
        if postcode and postcode != '':
            url = f"{url}&postcode={postcode}"
        if filters and filters != '':
            url = f"{url}&filters={filters}"
        if sortBySubject and sortBySubject == 'true':
            url = f"{url}&sortBySubject={sortBySubject}"
            if sortBySubjectLimit and sortBySubjectLimit != '':
                url = f"{url}&sortBySubjectLimit={sortBySubjectLimit}"

        return requests.request("POST", url, headers=headers, data=json.dumps(institution_dict))
