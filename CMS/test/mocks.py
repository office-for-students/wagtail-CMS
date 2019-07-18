import json
from requests.models import Response
from http import HTTPStatus


class CourseMocks:

    @classmethod
    def get_successful_course_load_content(cls):
        return {
            "id": "7948bc0c-a7c2-11e9-a181-186590d5a74b",
            "created_at": "2019-07-16T12:08:51.181524",
            "version": 1,
            "course": {
                "country": {
                    "code": "XH",
                    "name": "Scotland"
                },
                "distance_learning": {
                    "code": "0",
                    "label": "Course is availble other than by distance learning"
                },
                "foundation_year_availability": {
                    "code": "0",
                    "label": "Not available"
                },
                "honours_award_provision": "1",
                "institution": {
                    "pub_ukprn_name": "UNIVERSITY OF ABERDEEN",
                    "pub_ukprn": "10007783",
                    "ukprn_name": "UNIVERSITY OF ABERDEEN",
                    "ukprn": "10007783"
                },
                "kis_course_id": "C451",
                "length_of_course": {
                    "code": "5",
                    "label": "5 stages"
                },
                "links": {
                    "accommodation": [
                        {
                            "english": "http://www.abdn.ac.uk/accommodation"
                        },
                        {
                            "english": "http://www.abdn.ac.uk/accommodation"
                        }
                    ],
                    "assessment_method": {
                        "english": "http://www.abdn.ac.uk/prospectus/ugrad/study/C451"
                    },
                    "course_page": {
                        "english": "http://www.abdn.ac.uk/prospectus/ugrad/study/C451"
                    },
                    "employment_details": {
                        "english": "http://www.abdn.ac.uk/prospectus/ugrad/study/C451"
                    },
                    "financial_support_details": {
                        "english": "http://www.abdn.ac.uk/undergraduate/finance.php"
                    },
                    "learning_and_teaching_methods": {
                        "english": "http://www.abdn.ac.uk/prospectus/ugrad/study/C451"
                    },
                    "student_union": {
                        "english": "http://www.ausa.org.uk/"
                    }
                },
                "locations": [
                    {
                        "latitude": "57.156576",
                        "longitude": "-2.135668",
                        "name": {
                            "english": "Foresterhill"
                        }
                    },
                    {
                        "latitude": "57.165019",
                        "longitude": "-2.099122",
                        "name": {
                            "english": "Old Aberdeen"
                        }
                    }
                ],
                "mode": {
                    "code": "1",
                    "label": "Full-time"
                },
                "qualification": {
                    "code": "077",
                    "label": "MSci"
                },
                "sandwich_year": {
                    "code": "2",
                    "label": "Compulsory"
                },
                "title": {
                    "english": "Genetics (Immunology) with Industrial Placement"
                },
                "ucas_programme_id": "A33-F68",
                "year_abroad": {
                    "code": "0",
                    "label": "Not available"
                },
                "statistics": {
                    "continuation": [
                        {
                            "aggregation_level": 13,
                            "continuing_with_provider": 75,
                            "dormant": 0,
                            "gained": 20,
                            "left": 0,
                            "lower": 5,
                            "number_of_students": 20,
                            "subject": {
                                "code": "CAH03-01-07",
                                "english_label": "Genetics",
                                "welsh_label": "Geneteg"
                            },
                            "unavailable": {
                                "code": "0",
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Genetics."
                            }
                        }
                    ],
                    "employment": [
                        {
                            "aggregation_level": 23,
                            "assumed_to_be_unemployed": 0,
                            "in_study": 45,
                            "in_work": 55,
                            "in_work_and_study": 0,
                            "in_work_or_study": 100,
                            "not_available_for_work_or_study": 0,
                            "number_of_students": 15,
                            "response_rate": 80,
                            "subject": {
                                "code": "CAH03-01-07",
                                "english_label": "Genetics",
                                "welsh_label": "Geneteg"
                            },
                            "unavailable": {
                                "code": "0",
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Genetics."
                            }
                        }
                    ],
                    "entry": [
                        {
                            "a-level": 30,
                            "access": 0,
                            "aggregation_level": 13,
                            "another_higher_education_qualifications": 0,
                            "baccalaureate": 5,
                            "degree": 0,
                            "foundation": 0,
                            "none": 0,
                            "number_of_students": 30,
                            "other_qualifications": 65,
                            "subject": {
                                "code": "CAH03-01-07",
                                "english_label": "Genetics",
                                "welsh_label": "Geneteg"
                            },
                            "unavailable": {
                                "code": "0",
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Genetics."
                            }
                        }
                    ],
                    "job_type": [
                        {
                            "aggregation_level": 12,
                            "non_professional_or_managerial_jobs": 35,
                            "number_of_students": 25,
                            "professional_or_managerial_jobs": 65,
                            "resp_rate": 80,
                            "subject": {
                                "code": "CAH03-01",
                                "english_label": "Biosciences",
                                "welsh_label": "Biowyddorau"
                            },
                            "unavailable": {
                                "code": "0",
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Biosciences."
                            },
                            "unknown_professions": 0
                        }
                    ],
                    "salary": [
                        {
                            "aggregation_level": 12,
                            "higher_quartile": 22000,
                            "lower_quartile": 16000,
                            "number_of_graduates": 15,
                            "response_rate": 80,
                            "subject": {
                                "code": "CAH03-01",
                                "english_label": "Biosciences",
                                "welsh_label": "Biowyddorau"
                            },
                            "unavailable": {
                                "code": "0",
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Biosciences."
                            }
                        }
                    ]
                }
            }
        }

    @classmethod
    def get_successful_course_load_response(cls):
        response = Response()
        response.status_code = HTTPStatus.OK
        response._content = json.dumps(cls.get_successful_course_load_content()).encode('utf-8')
        return response


class SearchMocks:

    @classmethod
    def get_search_response_content(cls):
        return {
            "total_number_of_courses": 10,
            "total_results": 5,
            "items": [
                {
                    'id': 1,
                    'institution': 'Oxford',
                    'course_name': 'Farming'
                }
            ]
        }

    @classmethod
    def get_successful_search_response(cls):
        response = Response()
        response.status_code = HTTPStatus.OK
        response._content = json.dumps(cls.get_search_response_content()).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_search_response(cls):
        response = Response()
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        response._content = json.dumps(None).encode('utf-8')
        return response
