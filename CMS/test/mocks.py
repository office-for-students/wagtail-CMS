import json
from requests.models import Response
from http import HTTPStatus


class NewCourseFormatMocks:

    @classmethod
    def get_successful_course_load_content(cls):
        return {
            "_id": "6ae859c8-ca79-11ea-8811-acde48001122",
            "created_at": "2020-07-20T11:09:02.168754",
            "version": 37,
            "institution_id": "10006841",
            "course_id": "ART002-F-UOB-SX",
            "course_mode": 1,
            "partition_key": "37",
            "course": {
                "country": {
                    "code": "XF",
                    "name": "England"
                },
                "distance_learning": {
                    "code": 0,
                    "label": "Course is available other than by distance learning"
                },
                "foundation_year_availability": {
                    "code": 0,
                    "label": "Not available"
                },
                "honours_award_provision": 1,
                "institution": {
                    "pub_ukprn_name": "The University of Bolton",
                    "pub_ukprn_welsh_name": "The University of Bolton",
                    "pub_ukprn": "10006841",
                    "ukprn_name": "The University of Bolton",
                    "ukprn_welsh_name": "The University of Bolton",
                    "ukprn": "10006841"
                },
                "kis_course_id": "ART002-F-UOB-SX",
                "go_salary_inst": {
                    "unavail_reason": "0",
                    "pop": "15",
                    "resp_rate": "55",
                    "agg": "23",
                    "sbj": "CAH01-01-01",
                    "lq": "16000",
                    "med": "18000",
                    "uq": "21000",
                    "go_inst_prov_pc_uk": "100",
                    "go_inst_prov_pc_e": "80",
                    "go_inst_prov_pc_s": "5",
                    "go_inst_prov_pc_w": "15",
                    "go_inst_prov_pc_ni": "0",
                    "go_inst_prov_pc_nw": "0",
                    "go_inst_prov_pc_ne": "0",
                    "go_inst_prov_pc_em": "0",
                    "go_inst_prov_pc_wm": "0",
                    "go_inst_prov_pc_ee": "0",
                    "go_inst_prov_pc_se": "0",
                    "go_inst_prov_pc_sw": "0",
                    "go_inst_prov_pc_yh": "0",
                    "go_inst_prov_pc_lo": "0",
                    "go_inst_prov_pc_ed": "0",
                    "go_inst_prov_pc_gl": "0",
                    "go_inst_prov_pc_cf": "0",
                    "unavail_text_inst_level_eng": "This is the unavail message in ENGLISH for the GO institution panel.",
                    "unavail_text_inst_level_wls": "This is the unavail message in WELSH for the GO institution panel.",
                    "unavail_text_inst_level_2_eng": "This is the second unavail message in ENGLISH for the GO institution panel.",
                    "unavail_text_inst_level_2_wls": "This is the second unavail message in WELSH for the GO institution panel."
                },
                "leo3_inst": {
                    "unavail_reason": "0",
                    "pop": "110",
                    "resp_rate": "55",
                    "agg": "23",
                    "sbj": "CAH01-01-01",
                    "lq": "14500",
                    "med": "18000",
                    "uq": "24000",
                    "unavail_text_inst_level_eng": "This is the unavail message in ENGLISH for the LEO3 institution panel.",
                    "unavail_text_inst_level_wls": "This is the unavail message in WELSH for the LEO3 institution panel."
                 },
                "leo5_inst": {
                    "unavail_reason": "0",
                    "pop": "110",
                    "resp_rate": "55",
                    "agg": "23",
                    "sbj": "CAH01-01-01",
                    "lq": "14500",
                    "med": "18000",
                    "uq": "24000",
                    "unavail_text_inst_level_eng": "This is the unavail message in ENGLISH for the LEO5 institution panel.",
                    "unavail_text_inst_level_wls": "This is the unavail message in WELSH for the LEO5 institution panel."
                },
                "go_voice_work": [
                    {
                        "course_name": "Course 1",
                        "go_work_skills": "32",
                        "go_work_mean": "87",
                        "go_work_on_track": "50",
                        "go_work_pop": "60",
                        "go_work_resp_rate": "85"
                    },
                    {
                        "course_name": "Course 2",
                        "go_work_skills": "87",
                        "go_work_mean": "50",
                        "go_work_on_track": "32",
                        "go_work_pop": "85",
                        "go_work_resp_rate": "60"
                    }
                ],
                "length_of_course": {
                    "code": 3,
                    "label": "3 stages"
                },
                "links": {
                    "assessment_method": {
                        "english": "http://courses.bolton.ac.uk/course/ART002-F-UOB-SX/2020-21/#teaching-assessment"
                    },
                    "course_cost": {
                        "english": "http://courses.bolton.ac.uk/course/ART002-F-UOB-SX/2020-21/#fees-funding"
                    },
                    "course_page": {
                        "english": "http://courses.bolton.ac.uk/course/ART002-F-UOB-SX/2020-21/#course-details"
                    },
                    "employment_details": {
                        "english": "http://courses.bolton.ac.uk/course/ART002-F-UOB-SX/2020-21/#careers-employment"
                    },
                    "financial_support_details": {
                        "english": "http://www.bolton.ac.uk/kis"
                    },
                    "learning_and_teaching_methods": {
                        "english": "http://courses.bolton.ac.uk/course/ART002-F-UOB-SX/2020-21/#teaching-assessment"
                    },
                    "student_union": {
                        "english": "http://www.boltonsu.com/"
                    }
                },
                "locations": [
                    {
                        "links": {
                            "student_union": {
                                "english": "http://www.boltonsu.com/"
                            }
                        },
                        "latitude": "53.573515",
                        "longitude": "-2.436239",
                        "name": {
                            "english": "University of Bolton"
                        },
                        "ucas_course_id": "5318"
                    }
                ],
                "mode": {
                    "code": 1,
                    "label": "Full-time"
                },
                "qualification": {
                    "code": "000",
                    "label": "BA",
                    "level": "first-degree"
                },
                "sandwich_year": {
                    "code": 0,
                    "label": "Not available"
                },
                "subjects": [
                    {
                        "code": "CAH01-01-01",
                        "level": 3,
                        "english": "Graphical Design (non-specific)",
                        "welsh": "Gwyddorau meddygol (amhenodol)"
                    }
                ],
                "title": {
                    "english": "Graphic Design"
                },
                "ucas_programme_id": "A09-C13",
                "year_abroad": {
                    "code": 0,
                    "label": "Not available"
                },
                "statistics": {
                    "continuation": [
                        {
                            "aggregation_level": 14,
                            "continuing_with_provider": 85,
                            "dormant": 10,
                            "gained": 0,
                            "left": 10,
                            "lower": 0,
                            "number_of_students": 15
                        }
                    ],
                    "employment": [
                        {
                            "aggregation_level": 13,
                            "assumed_to_be_unemployed": 20,
                            "in_study": 15,
                            "in_work": 60,
                            "in_work_and_study": 5,
                            "in_work_or_study": 80,
                            "not_available_for_work_or_study": 5,
                            "number_of_students": 35,
                            "response_rate": 95,
                            "subject": {
                                "code": "CAH01-01-01",
                                "english_label": "Graphical Design (non-specific)",
                                "welsh_label": "Gwyddorau meddygol (amhenodol)"
                            },
                            "unavailable": {
                                "code": 1,
                                "reason_english": "The data displayed is from students on other courses in Graphical Design (non-specific) subject. There was not enough data to publish information specifically for this course. This is because the course has not yet run or has not been running long enough for this data to be available.",
                                "reason_welsh": "Nid oes data ar gael ar gyfer y cwrs hwn. Mae hyn oherwydd nad yw'r cwrs wedi'i gynnal eto neu am nad yw wedi cael ei gynnal yn ddigon hir i'r data hwn fod ar gael. Am y rheswm hwn, mae'r data a ddangosir ar gyfer myfyrwyr ar gyrsiau eraill mewn "
                            }
                        }
                    ],
                    "entry": [
                        {
                            "a-level": 75,
                            "access": 0,
                            "aggregation_level": 14,
                            "another_higher_education_qualifications": 25,
                            "baccalaureate": 0,
                            "degree": 0,
                            "foundation": 0,
                            "none": 0,
                            "number_of_students": 20,
                            "other_qualifications": 0
                        }
                    ],
                    "job_type": [
                        {
                            "aggregation_level": 13,
                            "non_professional_or_managerial_jobs": 45,
                            "number_of_students": 25,
                            "professional_or_managerial_jobs": 55,
                            "response_rate": 95,
                            "subject": {
                                "code": "CAH01-01-01",
                                "english_label": "Graphical Design (non-specific)",
                                "welsh_label": "Gwyddorau meddygol (amhenodol)"
                            },
                            "unavailable": {
                                "code": 1,
                                "reason_english": "The data displayed is from students on other courses in Graphical Design (non-specific) subject. There was not enough data to publish information specifically for this course. This is because the course has not yet run or has not been running long enough for this data to be available.",
                                "reason_welsh": "Nid oes data ar gael ar gyfer y cwrs hwn. Mae hyn oherwydd nad yw'r cwrs wedi'i gynnal eto neu am nad yw wedi cael ei gynnal yn ddigon hir i'r data hwn fod ar gael. Am y rheswm hwn, mae'r data a ddangosir ar gyfer myfyrwyr ar gyrsiau eraill mewn "
                            },
                            "unknown_professions": 0
                        }
                    ],
                    "job_list": [
                        {
                            "aggregation_level": 24,
                            "list": [
                                {
                                    "job": "Business, research and administrative professionals",
                                    "percentage_of_students": "65",
                                    "order": "1",
                                    "hss": 0
                                },
                                {
                                    "job": "Managers, directors and senior officials",
                                    "percentage_of_students": "10",
                                    "order": "2",
                                    "hss": 0
                                },
                                {
                                    "job": "Information technology and telecommunications professionals",
                                    "percentage_of_students": "5",
                                    "order": "3",
                                    "hss": 0
                                },
                                {
                                    "job": "Artistic, literary and media occupations",
                                    "percentage_of_students": "5",
                                    "order": "4",
                                    "hss": 1
                                },
                                {
                                    "job": "Business and public service associate professionals",
                                    "percentage_of_students": "5",
                                    "order": "5",
                                    "hss": 0
                                },
                                {
                                    "job": "Skilled trades occupations",
                                    "percentage_of_students": "5",
                                    "order": "6",
                                    "hss": 0
                                },
                                {
                                    "job": "Sales occupations",
                                    "percentage_of_students": "5",
                                    "order": "7",
                                    "hss": 1
                                },
                                {
                                    "job": "Customer service occupations",
                                    "percentage_of_students": "5",
                                    "order": "8",
                                    "hss": 1
                                }
                            ],
                            "number_of_students": 25,
                            "response_rate": 100,
                            "subject": {
                                "code": "CAH01-01-01",
                                "english_label": "Graphical Design (non-specific)",
                                "welsh_label": "Gwyddorau meddygol (amhenodol)"
                            },
                            "unavailable": {
                                "code": 1,
                                "reason_english": "The data displayed is from students on other courses in Graphical Design (non-specific) subject. There was not enough data to publish information specifically for this course. This is because the course has not yet run or has not been running long enough for this data to be available.",
                                "reason_welsh": "Nid oes data ar gael ar gyfer y cwrs hwn. Mae hyn oherwydd nad yw'r cwrs wedi'i gynnal eto neu am nad yw wedi cael ei gynnal yn ddigon hir i'r data hwn fod ar gael. Am y rheswm hwn, mae'r data a ddangosir ar gyfer myfyrwyr ar gyrsiau eraill mewn "
                            }
                        }
                    ],
                    "leo": [
                        {
                            "aggregation_level": 21,
                            "higher_quartile": 19500,
                            "lower_quartile": 11500,
                            "median": 15500,
                            "number_of_graduates": 175,
                            "subject": {
                                "code": "CAH01",
                                "english_label": "Medicine and dentistry",
                                "welsh_label": "Meddygaeth a deintyddiaeth"
                            }
                        }
                    ],
                    "nss": [
                        {
                            "aggregation_level": 14,
                            "number_of_students": 15,
                            "question_1": {
                                "description": "Staff are good at explaining things",
                                "agree_or_strongly_agree": 100
                            },
                            "question_2": {
                                "description": "Staff have made the subject interesting",
                                "agree_or_strongly_agree": 100
                            },
                            "question_3": {
                                "description": "The course is intellectually stimulating",
                                "agree_or_strongly_agree": 93
                            },
                            "question_4": {
                                "description": "My course has challenged me to achieve my best work",
                                "agree_or_strongly_agree": 93
                            },
                            "question_5": {
                                "description": "My course has provided me with opportunities to explore ideas or concepts in depth",
                                "agree_or_strongly_agree": 93
                            },
                            "question_6": {
                                "description": "My course has provided me with opportunities to bring information and ideas together from different topics",
                                "agree_or_strongly_agree": 93
                            },
                            "question_7": {
                                "description": "My course has provided me with opportunities to apply what I have learnt",
                                "agree_or_strongly_agree": 93
                            },
                            "question_8": {
                                "description": "The criteria used in marking have been clear in advance",
                                "agree_or_strongly_agree": 93
                            },
                            "question_9": {
                                "description": "Marking and assessment has been fair",
                                "agree_or_strongly_agree": 93
                            },
                            "question_10": {
                                "description": "Feedback on my work has been timely",
                                "agree_or_strongly_agree": 87
                            },
                            "question_11": {
                                "description": "I have received helpful comments on my work",
                                "agree_or_strongly_agree": 93
                            },
                            "question_12": {
                                "description": "I have been able to contact staff when I needed to",
                                "agree_or_strongly_agree": 93
                            },
                            "question_13": {
                                "description": "I have received sufficient advice and guidance in relation to my course",
                                "agree_or_strongly_agree": 93
                            },
                            "question_14": {
                                "description": "Good advice was available when I needed to make study choices on my course",
                                "agree_or_strongly_agree": 100
                            },
                            "question_15": {
                                "description": "The course is well organised and running smoothly",
                                "agree_or_strongly_agree": 100
                            },
                            "question_16": {
                                "description": "The timetable works efficiently for me",
                                "agree_or_strongly_agree": 87
                            },
                            "question_17": {
                                "description": "Any changes in the course or teaching have been communicated effectively",
                                "agree_or_strongly_agree": 93
                            },
                            "question_18": {
                                "description": "The IT resources and facilities provided have supported my learning well",
                                "agree_or_strongly_agree": 100
                            },
                            "question_19": {
                                "description": "The library resources (e.g. books, online services and learning spaces) have supported my learning well",
                                "agree_or_strongly_agree": 87
                            },
                            "question_20": {
                                "description": "I have been able to access course-specific resources (e.g. equipment, facilities, software, collections) when I needed to",
                                "agree_or_strongly_agree": 100
                            },
                            "question_21": {
                                "description": "I feel part of a community of staff and students",
                                "agree_or_strongly_agree": 87
                            },
                            "question_22": {
                                "description": "I have had the right opportunities to work with other students as part of my course",
                                "agree_or_strongly_agree": 87
                            },
                            "question_23": {
                                "description": "I have had the right opportunities to provide feedback on my course",
                                "agree_or_strongly_agree": 93
                            },
                            "question_24": {
                                "description": "Staff value students' views and opinions about the course",
                                "agree_or_strongly_agree": 100
                            },
                            "question_25": {
                                "description": "It is clear how students' feedback on the course has been acted on",
                                "agree_or_strongly_agree": 93
                            },
                            "question_26": {
                                "description": "The students' union (association or guild) effectively represents students' academic interests",
                                "agree_or_strongly_agree": 73
                            },
                            "question_27": {
                                "description": "Overall, I am satisfied with the quality of the course",
                                "agree_or_strongly_agree": 87
                            },
                            "response_rate": 79
                        }
                    ],
                    "salary": [
                        {
                            "aggregation_level": 13,
                            "higher_quartile": 20000,
                            "lower_quartile": 14000,
                            "median": 16000,
                            "number_of_graduates": 10,
                            "response_rate": 85,
                            "sector_higher_quartile": 20000,
                            "sector_lower_quartile": 16000,
                            "sector_median": 18000,
                            "subject": {
                                "code": "CAH01-01-01",
                                "english_label": "Graphical Design (non-specific)",
                                "welsh_label": "Gwyddorau meddygol (amhenodol)"
                            },
                            "unavailable": {
                                "code": 1,
                                "reason_english": "The data displayed is from students on other courses in Graphical Design (non-specific) subject. There was not enough data to publish information specifically for this course. This is because the course has not yet run or has not been running long enough for this data to be available.",
                                "reason_welsh": "Nid oes data ar gael ar gyfer y cwrs hwn. Mae hyn oherwydd nad yw'r cwrs wedi'i gynnal eto neu am nad yw wedi cael ei gynnal yn ddigon hir i'r data hwn fod ar gael. Am y rheswm hwn, mae'r data a ddangosir ar gyfer myfyrwyr ar gyrsiau eraill mewn "
                            }
                        }
                    ],
                    "tariff": [
                        {
                            "aggregation_level": 14,
                            "number_of_students": 15,
                            "tariffs": [
                                {
                                    "code": "T001",
                                    "description": "less than 48 tariff points",
                                    "entrants": 0
                                },
                                {
                                    "code": "T048",
                                    "description": "between 48 and 63 tariff points",
                                    "entrants": 0
                                },
                                {
                                    "code": "T064",
                                    "description": "between 64 and 79 tariff points",
                                    "entrants": 25
                                },
                                {
                                    "code": "T080",
                                    "description": "between 80 and 95 tariff points",
                                    "entrants": 0
                                },
                                {
                                    "code": "T096",
                                    "description": "between 96 and 111 tariff points",
                                    "entrants": 0
                                },
                                {
                                    "code": "T112",
                                    "description": "between 112 and 127 tariff points",
                                    "entrants": 30
                                },
                                {
                                    "code": "T128",
                                    "description": "between 128 and 143 tariff points",
                                    "entrants": 15
                                },
                                {
                                    "code": "T144",
                                    "description": "between 144 and 159 tariff points",
                                    "entrants": 0
                                },
                                {
                                    "code": "T160",
                                    "description": "between 160 and 175 tariff points",
                                    "entrants": 30
                                },
                                {
                                    "code": "T176",
                                    "description": "between 176 and 191 tariff points",
                                    "entrants": 0
                                },
                                {
                                    "code": "T192",
                                    "description": "between 192 and 207 tariff points",
                                    "entrants": 0
                                },
                                {
                                    "code": "T208",
                                    "description": "between 208 and 223 tariff points",
                                    "entrants": 0
                                },
                                {
                                    "code": "T224",
                                    "description": "between 224 and 239 tariff points",
                                    "entrants": 0
                                },
                                {
                                    "code": "T240",
                                    "description": "240 or more tariff points",
                                    "entrants": 0
                                }
                            ]
                        }
                    ]
                },
                "go_salary_sector": {
                    "unavail_reason": "0",
                    "pop": "15",
                    "resp_rate": "55",
                    "agg": "23",
                    "sbj": "CAH01-01-01",
                    "mode": "1",
                    "level": "2",
                    "lq_uk": "20000",
                    "med_uk": "22000",
                    "uq_uk": "28000",
                    "pop_uk": "290",
                    "resp_uk": "100",
                    "lq_e": "17000",
                    "med_e": "20000",
                    "uq_e": "24000",
                    "pop_e": "150",
                    "resp_e": "80",
                    "lq_s": "18000",
                    "med_s": "21000",
                    "uq_s": "25000",
                    "pop_s": "140",
                    "resp_s": "20",
                    "lq_w": "18000",
                    "med_w": "21000",
                    "uq_w": "25000",
                    "pop_w": "140",
                    "resp_w": "20",
                    "lq_ni": "18000",
                    "med_ni": "21000",
                    "uq_ni": "25000",
                    "pop_ni": "140",
                    "resp_ni": "20",
                    "lq_nw": "18000",
                    "med_nw": "21000",
                    "uq_nw": "25000",
                    "pop_nw": "140",
                    "resp_nw": "20",
                    "lq_ne": "18000",
                    "med_ne": "21000",
                    "uq_ne": "25000",
                    "pop_ne": "140",
                    "resp_ne": "20",
                    "lq_em": "18000",
                    "med_em": "21000",
                    "uq_em": "25000",
                    "pop_em": "140",
                    "resp_em": "20",
                    "lq_wm": "18000",
                    "med_wm": "21000",
                    "uq_wm": "25000",
                    "pop_wm": "140",
                    "resp_wm": "20",
                    "lq_ee": "18000",
                    "med_ee": "21000",
                    "uq_ee": "25000",
                    "pop_ee": "140",
                    "resp_ee": "20",
                    "lq_se": "18000",
                    "med_se": "21000",
                    "uq_se": "25000",
                    "pop_se": "140",
                    "resp_se": "20",
                    "lq_sw": "18000",
                    "med_sw": "21000",
                    "uq_sw": "25000",
                    "pop_sw": "140",
                    "resp_sw": "20",
                    "lq_yh": "18000",
                    "med_yh": "21000",
                    "uq_yh": "25000",
                    "pop_yh": "140",
                    "resp_yh": "20",
                    "lq_lo": "18000",
                    "med_lo": "21000",
                    "uq_lo": "25000",
                    "pop_lo": "140",
                    "resp_lo": "20",
                    "lq_ed": "18000",
                    "med_ed": "21000",
                    "uq_ed": "25000",
                    "pop_ed": "140",
                    "resp_ed": "20",
                    "lq_gl": "18000",
                    "med_gl": "21000",
                    "uq_gl": "25000",
                    "pop_gl": "140",
                    "resp_gl": "20",
                    "lq_cf": "18000",
                    "med_cf": "21000",
                    "uq_cf": "25000",
                    "pop_cf": "140",
                    "resp_cf": "20",
                    "unavail_text_sector_level_eng": "This is the unavail message in ENGLISH for the GO sector panel.",
                    "unavail_text_sector_level_wls": "This is the unavail message in WELSH for the GO sector panel.",
                    "unavail_text_non_nation_selected_eng": "This is the unavail message in ENGLISH for the GO institution panel if the user selects a non-nation region.",
                    "unavail_text_non_nation_selected_wls": "This is the unavail message in WELSH for the GO institution panel if the user selects a non-nation region."
                },
                "leo3_salary_sector": {
                    "unavail_reason": "0",
                    "pop": "15",
                    "resp_rate": "55",
                    "agg": "23",
                    "sbj": "CAH01-01-01",
                    "mode": "1",
                    "level": "2",
                    "lq_uk": "20000",
                    "med_uk": "22000",
                    "uq_uk": "28000",
                    "pop_uk": "290",
                    "resp_uk": "100",
                    "lq_e": "17000",
                    "med_e": "20000",
                    "uq_e": "24000",
                    "pop_e": "150",
                    "resp_e": "80",
                    "lq_s": "18000",
                    "med_s": "21000",
                    "uq_s": "25000",
                    "pop_s": "140",
                    "resp_s": "20",
                    "lq_w": "18000",
                    "med_w": "21000",
                    "uq_w": "25000",
                    "pop_w": "140",
                    "resp_w": "20",
                    "lq_ni": "18000",
                    "med_ni": "21000",
                    "uq_ni": "25000",
                    "pop_ni": "140",
                    "resp_ni": "20",
                    "lq_nw": "18000",
                    "med_nw": "21000",
                    "uq_nw": "25000",
                    "pop_nw": "140",
                    "resp_nw": "20",
                    "lq_ne": "18000",
                    "med_ne": "21000",
                    "uq_ne": "25000",
                    "pop_ne": "140",
                    "resp_ne": "20",
                    "lq_em": "18000",
                    "med_em": "21000",
                    "uq_em": "25000",
                    "pop_em": "140",
                    "resp_em": "20",
                    "lq_wm": "18000",
                    "med_wm": "21000",
                    "uq_wm": "25000",
                    "pop_wm": "140",
                    "resp_wm": "20",
                    "lq_ee": "18000",
                    "med_ee": "21000",
                    "uq_ee": "25000",
                    "pop_ee": "140",
                    "resp_ee": "20",
                    "lq_se": "18000",
                    "med_se": "21000",
                    "uq_se": "25000",
                    "pop_se": "140",
                    "resp_se": "20",
                    "lq_sw": "18000",
                    "med_sw": "21000",
                    "uq_sw": "25000",
                    "pop_sw": "140",
                    "resp_sw": "20",
                    "lq_yh": "18000",
                    "med_yh": "21000",
                    "uq_yh": "25000",
                    "pop_yh": "140",
                    "resp_yh": "20",
                    "lq_lo": "18000",
                    "med_lo": "21000",
                    "uq_lo": "25000",
                    "pop_lo": "140",
                    "resp_lo": "20",
                    "lq_ed": "18000",
                    "med_ed": "21000",
                    "uq_ed": "25000",
                    "pop_ed": "140",
                    "resp_ed": "20",
                    "lq_gl": "18000",
                    "med_gl": "21000",
                    "uq_gl": "25000",
                    "pop_gl": "140",
                    "resp_gl": "20",
                    "lq_cf": "18000",
                    "med_cf": "21000",
                    "uq_cf": "25000",
                    "pop_cf": "140",
                    "resp_cf": "20",
                    "unavail_text_sector_level_eng": "This is the unavail message in ENGLISH for the LEO3 sector panel.",
                    "unavail_text_sector_level_wls": "This is the unavail message in WELSH for the LEO3 sector panel.",
                    "unavail_text_ni_selected_eng": "This is the unavail message in ENGLISH for the LEO3 institution panel if the user selects NI.",
                    "unavail_text_ni_selected_wls": "This is the unavail message in WELSH for the LEO3 institution panel if the user selects NI."
                },
                "leo5_salary_sector": {
                    "unavail_reason": "0",
                    "pop": "15",
                    "resp_rate": "55",
                    "agg": "23",
                    "sbj": "CAH01-01-01",
                    "mode": "1",
                    "level": "2",
                    "lq_uk": "20000",
                    "med_uk": "22000",
                    "uq_uk": "28000",
                    "pop_uk": "290",
                    "resp_uk": "100",
                    "lq_e": "17000",
                    "med_e": "20000",
                    "uq_e": "24000",
                    "pop_e": "150",
                    "resp_e": "80",
                    "lq_s": "18000",
                    "med_s": "21000",
                    "uq_s": "25000",
                    "pop_s": "140",
                    "resp_s": "20",
                    "lq_w": "18000",
                    "med_w": "21000",
                    "uq_w": "25000",
                    "pop_w": "140",
                    "resp_w": "20",
                    "lq_ni": "18000",
                    "med_ni": "21000",
                    "uq_ni": "25000",
                    "pop_ni": "140",
                    "resp_ni": "20",
                    "lq_nw": "18000",
                    "med_nw": "21000",
                    "uq_nw": "25000",
                    "pop_nw": "140",
                    "resp_nw": "20",
                    "lq_ne": "18000",
                    "med_ne": "21000",
                    "uq_ne": "25000",
                    "pop_ne": "140",
                    "resp_ne": "20",
                    "lq_em": "18000",
                    "med_em": "21000",
                    "uq_em": "25000",
                    "pop_em": "140",
                    "resp_em": "20",
                    "lq_wm": "18000",
                    "med_wm": "21000",
                    "uq_wm": "25000",
                    "pop_wm": "140",
                    "resp_wm": "20",
                    "lq_ee": "18000",
                    "med_ee": "21000",
                    "uq_ee": "25000",
                    "pop_ee": "140",
                    "resp_ee": "20",
                    "lq_se": "18000",
                    "med_se": "21000",
                    "uq_se": "25000",
                    "pop_se": "140",
                    "resp_se": "20",
                    "lq_sw": "18000",
                    "med_sw": "21000",
                    "uq_sw": "25000",
                    "pop_sw": "140",
                    "resp_sw": "20",
                    "lq_yh": "18000",
                    "med_yh": "21000",
                    "uq_yh": "25000",
                    "pop_yh": "140",
                    "resp_yh": "20",
                    "lq_lo": "18000",
                    "med_lo": "21000",
                    "uq_lo": "25000",
                    "pop_lo": "140",
                    "resp_lo": "20",
                    "lq_ed": "18000",
                    "med_ed": "21000",
                    "uq_ed": "25000",
                    "pop_ed": "140",
                    "resp_ed": "20",
                    "lq_gl": "18000",
                    "med_gl": "21000",
                    "uq_gl": "25000",
                    "pop_gl": "140",
                    "resp_gl": "20",
                    "lq_cf": "18000",
                    "med_cf": "21000",
                    "uq_cf": "25000",
                    "pop_cf": "140",
                    "resp_cf": "20",
                    "unavail_text_sector_level_eng": "This is the unavail message in ENGLISH for the LEO5 sector panel.",
                    "unavail_text_sector_level_wls": "This is the unavail message in WELSH for the LEO5 sector panel.",
                    "unavail_text_ni_selected_eng": "This is the unavail message in ENGLISH for the LEO5 institution panel if the user selects NI.",
                    "unavail_text_ni_selected_wls": "This is the unavail message in WELSH for the LEO5 institution panel if the user selects NI."
                }
            },
            "id": "da1abf3b-1129-88bc-fe38-41a2f1ce3991",
            "_rid": "isg9AIMJBtAIYgAAAAAAAA==",
            "_self": "dbs/isg9AA==/colls/isg9AIMJBtA=/docs/isg9AIMJBtAIYgAAAAAAAA==/",
            "_etag": "\"e100ce31-0000-1100-0000-5f157b650000\"",
            "_attachments": "attachments/",
            "_ts": 1595243365
        }

    @classmethod
    def get_successful_course_load_response(cls):
        response = Response()
        response.status_code = HTTPStatus.OK
        response._content = json.dumps(cls.get_successful_course_load_content()).encode('utf-8')
        return response


class CourseMocks:

    @classmethod
    def get_successful_course_load_content(cls):
        return {
            "id": "4fe3a37a-ac62-11e9-aa9f-186590d5a74b",
            "created_at": "2019-07-22T09:23:05.860230",
            "version": 1,
            "course": {
                "accreditations": [
                    {
                        "type": "09904",
                        "accreditor_url": "http://www.engc.org.uk/informationfor/students-apprentices-and-graduates/",
                        "text": {
                            "english": "Accredited by the Institution of Mechanical Engineers (IMechE) on behalf of the Engineering Council for the purposes of fully meeting the academic requirements for registration as an Engineering Technician and partially meeting the academic requirement for registration as an Incorporated Engineer.",
                            "welsh": "Hachredu gan Sefydliad y Peirianwyr Mecanyddol (IMechE) ar ran y Cyngor Peirianneg at ddibenion llawn cwrdd â'r gofynion academaidd ar gyfer cofrestru fel Technegydd Peirianneg a rhannol gwrdd â'r gofynion academaidd ar gyfer cofrestru fel Peiriannydd Corfforedig."
                        },
                        "url": {
                            "english": "http://www.engc.org.uk/informationfor/students-apprentices-and-graduates/"
                        },
                        "dependent_on": {
                            "code": "1",
                            "label": "Accreditation is dependent on student choice"
                        }
                    },
                    {
                        "type": "09404",
                        "accreditor_url": "http://www.engc.org.uk/informationfor/students-apprentices-and-graduates/",
                        "text": {
                            "english": "Accredited by the Institution of Engineering and Technology (IET) on behalf of the Engineering Council for the purposes of fully meeting the academic requirements for registration as an Engineering Technician and partially meeting the academic requirement for registration as an Incorporated Engineer.",
                            "welsh": "Achrededig ganSefydliad Peirianneg a Thechnoleg (IET) ar ran y Cyngor Peirianneg at bwrpasau cwrdd yn rhannol â'r gofyniad academaidd ar gyfer cofrestru fel Peiriannydd Corfforedig"
                        },
                        "url": {
                            "english": "http://www.engc.org.uk/informationfor/students-apprentices-and-graduates/"
                        },
                        "dependent_on": {
                            "code": "1",
                            "label": "Accreditation is dependent on student choice"
                        }
                    }
                ],
                "application_provider": "10004930",
                "country": {
                    "code": "XF",
                    "name": "England"
                },
                "distance_learning": {
                    "code": "0",
                    "label": "Course is availble other than by distance learning"
                },
                "foundation_year_availability": {
                    "code": "0",
                    "label": "Not available"
                },
                "honours_award_provision": "0",
                "institution": {
                    "pub_ukprn_name": "ABINGDON AND WITNEY COLLEGE",
                    "pub_ukprn": "10000055",
                    "ukprn_name": "ABINGDON AND WITNEY COLLEGE",
                    "ukprn": "10000055"
                },
                "kis_course_id": "AB20",
                "length_of_course": {
                    "code": "2",
                    "label": "2 stages"
                },
                "links": {
                    "assessment_method": {
                        "english": "http://www.abingdon-witney.ac.uk/course/?code=EHWE103P&year=A18/19&title=Animal+Behaviour+and+Welfare%2C+Foundation+Degree+"
                    },
                    "course_page": {
                        "english": "http://www.abingdon-witney.ac.uk/course/?code=EHWE103P&year=A18/19&title=Animal+Behaviour+and+Welfare%2C+Foundation+Degree+"
                    },
                    "employment_details": {
                        "english": "http://www.abingdon-witney.ac.uk/course/?code=EHWE103P&year=A18/19&title=Animal+Behaviour+and+Welfare%2C+Foundation+Degree+"
                    },
                    "financial_support_details": {
                        "english": "http://www.brookes.ac.uk/studying-at-brookes/finance/undergraduate-finance---uk-and-eu-students/financial-support/financial-support-uk-eu-2018-19/"
                    },
                    "learning_and_teaching_methods": {
                        "english": "http://www.abingdon-witney.ac.uk/course/?code=EHWE103P&year=A18/19&title=Animal+Behaviour+and+Welfare%2C+Foundation+Degree+"
                    },

                },
                "locations": [
                    {
                        "latitude": "51.8202",
                        "longitude": "-1.477227",
                        "name": {
                            "english": "Abingdon &amp; Witney College (Common Leys Campus)"
                        },
                        'links': {
                            "accommodation": {
                                "english": "http://www.brookes.ac.uk/studying-at-brookes/accommodation/halls-in-detail/"
                            },
                            "student_union": {
                                "english": "http://www.nus.org.uk/en/students-unions/abingdon-and-witney-college-students-union/"
                            }
                        }
                    }
                ],
                "mode": {
                    "code": "1",
                    "label": "Full-time"
                },
                "qualification": {
                    "code": "036",
                    "label": "FdSc"
                },
                "sandwich_year": {
                    "code": "0",
                    "label": "Not available"
                },
                "title": {
                    "english": "Animal Behaviour and Welfare"
                },
                "year_abroad": {
                    "code": "0",
                    "label": "Not available"
                },
                "statistics": {
                    "continuation": [
                        {
                            "aggregation_level": 13,
                            "continuing_with_provider": 100,
                            "dormant": 0,
                            "gained": 0,
                            "left": 0,
                            "lower": 0,
                            "number_of_students": 15,
                            "subject": {
                                "code": "CAH09-01-01",
                                "english_label": "Mathematics",
                                "welsh_label": "Mathemateg"
                            },
                            "unavailable": {
                                "code": 0,
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Mathematics."
                            }
                        },
                        {
                            "aggregation_level": 13,
                            "continuing_with_provider": 100,
                            "dormant": 0,
                            "gained": 0,
                            "left": 0,
                            "lower": 0,
                            "number_of_students": 15,
                            "subject": {
                                "code": "CAH09-01-01",
                                "english_label": "Mathematics",
                                "welsh_label": "Mathemateg"
                            },
                            "unavailable": {
                                "code": 0,
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Mathematics."
                            }
                        }
                    ],
                    "employment": [
                        {
                            "aggregation_level": 13,
                            "assumed_to_be_unemployed": 5,
                            "in_study": 80,
                            "in_work": 5,
                            "in_work_and_study": 5,
                            "in_work_or_study": 95,
                            "not_available_for_work_or_study": 0,
                            "number_of_students": 15,
                            "response_rate": 100,
                            "subject": {
                                "code": "CAH09-01-01",
                                "english_label": "Mathematics",
                                "welsh_label": "Mathemateg"
                            },
                            "unavailable": {
                                "code": 0,
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Mathematics."
                            }
                        },
                        {
                            "aggregation_level": 13,
                            "assumed_to_be_unemployed": 5,
                            "in_study": 80,
                            "in_work": 5,
                            "in_work_and_study": 5,
                            "in_work_or_study": 95,
                            "not_available_for_work_or_study": 0,
                            "number_of_students": 15,
                            "response_rate": 100,
                            "subject": {
                                "code": "CAH09-01-01",
                                "english_label": "Mathematics",
                                "welsh_label": "Mathemateg"
                            },
                            "unavailable": {
                                "code": 0,
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Mathematics."
                            }
                        }
                    ],
                    "entry": [
                        {
                            "a-level": 65,
                            "access": 0,
                            "aggregation_level": 13,
                            "another_higher_education_qualifications": 15,
                            "baccalaureate": 5,
                            "degree": 5,
                            "foundation": 0,
                            "none": 5,
                            "number_of_students": 20,
                            "other_qualifications": 0,
                            "subject": {
                                "code": "CAH09-01-01",
                                "english_label": "Mathematics",
                                "welsh_label": "Mathemateg"
                            },
                            "unavailable": {
                                "code": 0,
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Mathematics."
                            }
                        },
                        {
                            "a-level": 70,
                            "access": 0,
                            "aggregation_level": 13,
                            "another_higher_education_qualifications": 15,
                            "baccalaureate": 5,
                            "degree": 5,
                            "foundation": 0,
                            "none": 5,
                            "number_of_students": 20,
                            "other_qualifications": 0,
                            "subject": {
                                "code": "CAH09-01-01",
                                "english_label": "Mathematics",
                                "welsh_label": "Mathemateg"
                            },
                            "unavailable": {
                                "code": 0,
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Mathematics."
                            }
                        }
                    ],
                    "job_type": [
                        {
                            "aggregation_level": 12,
                            "non_professional_or_managerial_jobs": 35,
                            "number_of_students": 25,
                            "professional_or_managerial_jobs": 65,
                            "response_rate": 80,
                            "unavailable": {
                                "code": "0",
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Biosciences."
                            },
                            "unknown_professions": 0,
                            "subject": {
                                "code": "CAH09-01-01",
                                "english_label": "Mathematics",
                                "welsh_label": "Mathemateg"
                            }
                        },
                        {
                            "aggregation_level": 12,
                            "non_professional_or_managerial_jobs": 35,
                            "number_of_students": 25,
                            "professional_or_managerial_jobs": 65,
                            "response_rate": 80,
                            "unavailable": {
                                "code": "0",
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Biosciences."
                            },
                            "unknown_professions": 0,
                            "subject": {
                                "code": "CAH09-01-01",
                                "english_label": "Mathematics",
                                "welsh_label": "Mathemateg"
                            }
                        }
                    ],
                    "job_list": [
                        {
                            "aggregation_level": 13,
                            "list": [
                                {
                                    "job": "Elementary occupations",
                                    "percentage_of_students": "20",
                                    "order": "1"
                                },
                                {
                                    "job": "Business and public service associate professionals",
                                    "percentage_of_students": "15",
                                    "order": "2"
                                },
                                {
                                    "job": "Managers, directors and senior officials",
                                    "percentage_of_students": "10",
                                    "order": "3"
                                },
                                {
                                    "job": "Business, research and administrative professionals",
                                    "percentage_of_students": "10",
                                    "order": "4"
                                },
                                {
                                    "job": "Teaching and educational professionals",
                                    "percentage_of_students": "5",
                                    "order": "5"
                                },
                                {
                                    "job": "Information technology and telecommunications professionals",
                                    "percentage_of_students": "5",
                                    "order": "6"
                                },
                                {
                                    "job": "Architects, town planners and surveyors",
                                    "percentage_of_students": "5",
                                    "order": "7"
                                },
                                {
                                    "job": "Librarians and related professionals",
                                    "percentage_of_students": "5",
                                    "order": "8"
                                },
                                {
                                    "job": "Sports and fitness occupations",
                                    "percentage_of_students": "5",
                                    "order": "9"
                                },
                                {
                                    "job": "Administrative occupations",
                                    "percentage_of_students": "5",
                                    "order": "10"
                                }
                            ],
                            "number_of_students": 20,
                            "response_rate": 85,
                            "subject": {
                                "code": "CAH09-01-01",
                                "english_label": "Mathematics",
                                "welsh_label": "Mathemateg"
                            },
                            "unavailable": {
                                "code": 0,
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Mathematics."
                            }
                        },
                        {
                            "aggregation_level": 13,
                            "list": [
                                {
                                    "job": "Elementary occupations",
                                    "percentage_of_students": "20",
                                    "order": "1"
                                },
                                {
                                    "job": "Business and public service associate professionals",
                                    "percentage_of_students": "15",
                                    "order": "2"
                                },
                                {
                                    "job": "Managers, directors and senior officials",
                                    "percentage_of_students": "10",
                                    "order": "3"
                                },
                                {
                                    "job": "Business, research and administrative professionals",
                                    "percentage_of_students": "10",
                                    "order": "4"
                                },
                                {
                                    "job": "Teaching and educational professionals",
                                    "percentage_of_students": "5",
                                    "order": "5"
                                },
                                {
                                    "job": "Information technology and telecommunications professionals",
                                    "percentage_of_students": "5",
                                    "order": "6"
                                },
                                {
                                    "job": "Architects, town planners and surveyors",
                                    "percentage_of_students": "5",
                                    "order": "7"
                                },
                                {
                                    "job": "Librarians and related professionals",
                                    "percentage_of_students": "5",
                                    "order": "8"
                                },
                                {
                                    "job": "Sports and fitness occupations",
                                    "percentage_of_students": "5",
                                    "order": "9"
                                },
                                {
                                    "job": "Administrative occupations",
                                    "percentage_of_students": "5",
                                    "order": "10"
                                }
                            ],
                            "number_of_students": 20,
                            "response_rate": 85,
                            "subject": {
                                "code": "CAH09-01-01",
                                "english_label": "Mathematics",
                                "welsh_label": "Mathemateg"
                            },
                            "unavailable": {
                                "code": 0,
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Mathematics."
                            }
                        }
                    ],
                    "nhs_nss": [
                        {
                            "aggregation_level": 13,
                            "number_of_students": 11111165,
                            "question_1": {
                                "description": "I received sufficient preparatory information prior to my placement(s)",
                                "agree_or_strongly_agree": 92
                            },
                            "question_2": {
                                "description": "I was allocated placement(s) suitable for my course",
                                "agree_or_strongly_agree": 97
                            },
                            "question_3": {
                                "description": "I received appropriate supervision on placement(s)",
                                "agree_or_strongly_agree": 111189
                            },
                            "question_4": {
                                "description": "I was given opportunities to meet my required practice learning outcomes/competences",
                                "agree_or_strongly_agree": 94
                            },
                            "question_5": {
                                "description": "My contribution during placement(s) as part of a clinical team was valued",
                                "agree_or_strongly_agree": 94
                            },
                            "question_6": {
                                "description": "My practice supervisor(s) understood how my placement(s) related to the broader requirements of my course",
                                "agree_or_strongly_agree": 94
                            },
                            "response_rate": 97,
                            "subject": {
                                "code": "CAH09-01-02",
                                "english_label": "Mathematics",
                                "welsh_label": "Mathemateg"
                            },
                            "unavailable": {
                                "code": 0,
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Mathematics."
                            }
                        },
                        {
                            "aggregation_level": 13,
                            "number_of_students": 65,
                            "question_1": {
                                "description": "I received sufficient preparatory information prior to my placement(s)",
                                "agree_or_strongly_agree": 92
                            },
                            "question_2": {
                                "description": "I was allocated placement(s) suitable for my course",
                                "agree_or_strongly_agree": 97
                            },
                            "question_3": {
                                "description": "I received appropriate supervision on placement(s)",
                                "agree_or_strongly_agree": 89
                            },
                            "question_4": {
                                "description": "I was given opportunities to meet my required practice learning outcomes/competences",
                                "agree_or_strongly_agree": 94
                            },
                            "question_5": {
                                "description": "My contribution during placement(s) as part of a clinical team was valued",
                                "agree_or_strongly_agree": 94
                            },
                            "question_6": {
                                "description": "My practice supervisor(s) understood how my placement(s) related to the broader requirements of my course",
                                "agree_or_strongly_agree": 94
                            },
                            "response_rate": 97,
                            "subject": {
                                "code": "CAH09-01-01",
                                "english_label": "Mathematics",
                                "welsh_label": "Mathemateg"
                            },
                            "unavailable": {
                                "code": 0,
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Mathematics."
                            }
                        }
                    ],
                    "nss": [
                        {
                            "aggregation_level": 13,
                            "number_of_students": 13,
                            "question_1": {
                                "description": "Staff are good at explaining things",
                                "agree_or_strongly_agree": 92
                            },
                            "question_2": {
                                "description": "Staff have made the subject interesting",
                                "agree_or_strongly_agree": 100
                            },
                            "question_3": {
                                "description": "The course is intellectually stimulating",
                                "agree_or_strongly_agree": 69
                            },
                            "question_4": {
                                "description": "My course has challenged me to achieve my best work",
                                "agree_or_strongly_agree": 92
                            },
                            "question_5": {
                                "description": "My course has provided me with opportunities to explore ideas or concepts in depth",
                                "agree_or_strongly_agree": 85
                            },
                            "question_6": {
                                "description": "My course has provided me with opportunities to bring information and ideas together from different topics",
                                "agree_or_strongly_agree": 92
                            },
                            "question_7": {
                                "description": "My course has provided me with opportunities to apply what I have learnt",
                                "agree_or_strongly_agree": 77
                            },
                            "question_8": {
                                "description": "The criteria used in marking have been clear in advance",
                                "agree_or_strongly_agree": 77
                            },
                            "question_9": {
                                "description": "Marking and assessment has been fair",
                                "agree_or_strongly_agree": 62
                            },
                            "question_10": {
                                "description": "Feedback on my work has been timely",
                                "agree_or_strongly_agree": 69
                            },
                            "question_11": {
                                "description": "I have received helpful comments on my work",
                                "agree_or_strongly_agree": 85
                            },
                            "question_12": {
                                "description": "I have been able to contact staff when I needed to",
                                "agree_or_strongly_agree": 62
                            },
                            "question_13": {
                                "description": "I have received sufficient advice and guidance in relation to my course",
                                "agree_or_strongly_agree": 77
                            },
                            "question_14": {
                                "description": "Good advice was available when I needed to make study choices on my course",
                                "agree_or_strongly_agree": 77
                            },
                            "question_15": {
                                "description": "The course is well organised and running smoothly",
                                "agree_or_strongly_agree": 54
                            },
                            "question_16": {
                                "description": "The timetable works efficiently for me",
                                "agree_or_strongly_agree": 85
                            },
                            "question_17": {
                                "description": "Any changes in the course or teaching have been communicated effectively",
                                "agree_or_strongly_agree": 77
                            },
                            "question_18": {
                                "description": "The IT resources and facilities provided have supported my learning well",
                                "agree_or_strongly_agree": 42
                            },
                            "question_19": {
                                "description": "The library resources (e.g. books, online services and learning spaces) have supported my learning well",
                                "agree_or_strongly_agree": 85
                            },
                            "question_20": {
                                "description": "I have been able to access course-specific resources (e.g. equipment, facilities, software, collections) when I needed to",
                                "agree_or_strongly_agree": 77
                            },
                            "question_21": {
                                "description": "I feel part of a community of staff and students",
                                "agree_or_strongly_agree": 69
                            },
                            "question_22": {
                                "description": "I have had the right opportunities to work with other students as part of my course",
                                "agree_or_strongly_agree": 85
                            },
                            "question_23": {
                                "description": "I have had the right opportunities to provide feedback on my course",
                                "agree_or_strongly_agree": 77
                            },
                            "question_24": {
                                "description": "Staff value students' views and opinions about the course",
                                "agree_or_strongly_agree": 85
                            },
                            "question_25": {
                                "description": "It is clear how students' feedback on the course has been acted on",
                                "agree_or_strongly_agree": 69
                            },
                            "question_26": {
                                "description": "The students' union (association or guild) effectively represents students' academic interests",
                                "agree_or_strongly_agree": 0
                            },
                            "question_27": {
                                "description": "Overall, I am satisfied with the quality of the course",
                                "agree_or_strongly_agree": 85
                            },
                            "response_rate": 93,
                            "subject": {
                                "code": "CAH09-01-01",
                                "english_label": "Mathematics",
                                "welsh_label": "Mathemateg"
                            },
                            "unavailable": {
                                "code": 0,
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Mathematics."
                            }
                        },
                        {
                            "aggregation_level": 13,
                            "number_of_students": 13,
                            "question_1": {
                                "description": "Staff are good at explaining things",
                                "agree_or_strongly_agree": 92
                            },
                            "question_2": {
                                "description": "Staff have made the subject interesting",
                                "agree_or_strongly_agree": 100
                            },
                            "question_3": {
                                "description": "The course is intellectually stimulating",
                                "agree_or_strongly_agree": 69
                            },
                            "question_4": {
                                "description": "My course has challenged me to achieve my best work",
                                "agree_or_strongly_agree": 92
                            },
                            "question_5": {
                                "description": "My course has provided me with opportunities to explore ideas or concepts in depth",
                                "agree_or_strongly_agree": 85
                            },
                            "question_6": {
                                "description": "My course has provided me with opportunities to bring information and ideas together from different topics",
                                "agree_or_strongly_agree": 92
                            },
                            "question_7": {
                                "description": "My course has provided me with opportunities to apply what I have learnt",
                                "agree_or_strongly_agree": 77
                            },
                            "question_8": {
                                "description": "The criteria used in marking have been clear in advance",
                                "agree_or_strongly_agree": 77
                            },
                            "question_9": {
                                "description": "Marking and assessment has been fair",
                                "agree_or_strongly_agree": 62
                            },
                            "question_10": {
                                "description": "Feedback on my work has been timely",
                                "agree_or_strongly_agree": 69
                            },
                            "question_11": {
                                "description": "I have received helpful comments on my work",
                                "agree_or_strongly_agree": 85
                            },
                            "question_12": {
                                "description": "I have been able to contact staff when I needed to",
                                "agree_or_strongly_agree": 62
                            },
                            "question_13": {
                                "description": "I have received sufficient advice and guidance in relation to my course",
                                "agree_or_strongly_agree": 77
                            },
                            "question_14": {
                                "description": "Good advice was available when I needed to make study choices on my course",
                                "agree_or_strongly_agree": 77
                            },
                            "question_15": {
                                "description": "The course is well organised and running smoothly",
                                "agree_or_strongly_agree": 54
                            },
                            "question_16": {
                                "description": "The timetable works efficiently for me",
                                "agree_or_strongly_agree": 85
                            },
                            "question_17": {
                                "description": "Any changes in the course or teaching have been communicated effectively",
                                "agree_or_strongly_agree": 77
                            },
                            "question_18": {
                                "description": "The IT resources and facilities provided have supported my learning well",
                                "agree_or_strongly_agree": 42
                            },
                            "question_19": {
                                "description": "The library resources (e.g. books, online services and learning spaces) have supported my learning well",
                                "agree_or_strongly_agree": 85
                            },
                            "question_20": {
                                "description": "I have been able to access course-specific resources (e.g. equipment, facilities, software, collections) when I needed to",
                                "agree_or_strongly_agree": 77
                            },
                            "question_21": {
                                "description": "I feel part of a community of staff and students",
                                "agree_or_strongly_agree": 69
                            },
                            "question_22": {
                                "description": "I have had the right opportunities to work with other students as part of my course",
                                "agree_or_strongly_agree": 85
                            },
                            "question_23": {
                                "description": "I have had the right opportunities to provide feedback on my course",
                                "agree_or_strongly_agree": 77
                            },
                            "question_24": {
                                "description": "Staff value students' views and opinions about the course",
                                "agree_or_strongly_agree": 85
                            },
                            "question_25": {
                                "description": "It is clear how students' feedback on the course has been acted on",
                                "agree_or_strongly_agree": 69
                            },
                            "question_26": {
                                "description": "The students' union (association or guild) effectively represents students' academic interests",
                                "agree_or_strongly_agree": 0
                            },
                            "question_27": {
                                "description": "Overall, I am satisfied with the quality of the course",
                                "agree_or_strongly_agree": 85
                            },
                            "response_rate": 93,
                            "subject": {
                                "code": "CAH09-01-02",
                                "english_label": "Mathematics",
                                "welsh_label": "Mathemateg"
                            },
                            "unavailable": {
                                "code": 0,
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Mathematics."
                            }
                        }
                    ],
                    "salary": [
                        {
                            "aggregation_level": 13,
                            "higher_quartile": 19000,
                            "lower_quartile": 16000,
                            "median": 18000,
                            "number_of_graduates": 15,
                            "response_rate": 60,
                            "sector_higher_quartile": 21000,
                            "sector_lower_quartile": 16000,
                            "sector_median": 18000,
                            "subject": {
                                "code": "CAH18-01-05",
                                "english_label": "Media studies",
                                "welsh_label": "Astudiaethau cyfryngau"
                            },
                            "unavailable": {
                                "code": 0,
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Media studies."
                            }
                        },
                        {
                            "aggregation_level": 13,
                            "higher_quartile": 19000,
                            "lower_quartile": 16000,
                            "median": 18000,
                            "number_of_graduates": 15,
                            "response_rate": 60,
                            "sector_higher_quartile": 21000,
                            "sector_lower_quartile": 16000,
                            "sector_median": 18000,
                            "subject": {
                                "code": "CAH18-01-05",
                                "english_label": "Media studies",
                                "welsh_label": "Astudiaethau cyfryngau"
                            },
                            "unavailable": {
                                "code": 0,
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Media studies."
                            }
                        }
                    ],
                    "tariff": [
                        {
                            "aggregation": "13",
                            "number_of_students": "10",
                            "tariffs": [
                                {
                                    "code": "T001",
                                    "description": "less than 48 tariff points",
                                    "entrants": "20"
                                },
                                {
                                    "code": "T048",
                                    "description": "between 48 and 63 tariff points",
                                    "entrants": "0"
                                },
                                {
                                    "code": "T064",
                                    "description": "between 64 and 79 tariff points",
                                    "entrants": "20"
                                },
                                {
                                    "code": "T080",
                                    "description": "between 80 and 95 tariff points",
                                    "entrants": "30"
                                },
                                {
                                    "code": "T096",
                                    "description": "between 96 and 111 tariff points",
                                    "entrants": "0"
                                },
                                {
                                    "code": "T112",
                                    "description": "between 112 and 127 tariff points",
                                    "entrants": "0"
                                },
                                {
                                    "code": "T128",
                                    "description": "between 128 and 143 tariff points",
                                    "entrants": "10"
                                },
                                {
                                    "code": "T144",
                                    "description": "between 144 and 159 tariff points",
                                    "entrants": "0"
                                },
                                {
                                    "code": "T160",
                                    "description": "between 160 and 175 tariff points",
                                    "entrants": "10"
                                },
                                {
                                    "code": "T176",
                                    "description": "between 176 and 191 tariff points",
                                    "entrants": "0"
                                },
                                {
                                    "code": "T192",
                                    "description": "between 192 and 207 tariff points",
                                    "entrants": "0"
                                },
                                {
                                    "code": "T208",
                                    "description": "between 208 and 223 tariff points",
                                    "entrants": "10"
                                },
                                {
                                    "code": "T224",
                                    "description": "between 224 and 239 tariff points",
                                    "entrants": "0"
                                },
                                {
                                    "code": "T240",
                                    "description": "240 or more tariff points",
                                    "entrants": "0"
                                }
                            ],
                            "subject": {
                                "code": "CAH09-01-01",
                                "english_label": "Mathematics",
                                "welsh_label": "Mathemateg"
                            },
                            "unavailable": {
                                "code": 0,
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Mathematics."
                            }
                        },
                        {
                            "aggregation": "13",
                            "number_of_students": "10",
                            "tariffs": [
                                {
                                    "code": "T001",
                                    "description": "less than 48 tariff points",
                                    "entrants": "20"
                                },
                                {
                                    "code": "T048",
                                    "description": "between 48 and 63 tariff points",
                                    "entrants": "0"
                                },
                                {
                                    "code": "T064",
                                    "description": "between 64 and 79 tariff points",
                                    "entrants": "20"
                                },
                                {
                                    "code": "T080",
                                    "description": "between 80 and 95 tariff points",
                                    "entrants": "30"
                                },
                                {
                                    "code": "T096",
                                    "description": "between 96 and 111 tariff points",
                                    "entrants": "0"
                                },
                                {
                                    "code": "T112",
                                    "description": "between 112 and 127 tariff points",
                                    "entrants": "0"
                                },
                                {
                                    "code": "T128",
                                    "description": "between 128 and 143 tariff points",
                                    "entrants": "10"
                                },
                                {
                                    "code": "T144",
                                    "description": "between 144 and 159 tariff points",
                                    "entrants": "0"
                                },
                                {
                                    "code": "T160",
                                    "description": "between 160 and 175 tariff points",
                                    "entrants": "10"
                                },
                                {
                                    "code": "T176",
                                    "description": "between 176 and 191 tariff points",
                                    "entrants": "0"
                                },
                                {
                                    "code": "T192",
                                    "description": "between 192 and 207 tariff points",
                                    "entrants": "0"
                                },
                                {
                                    "code": "T208",
                                    "description": "between 208 and 223 tariff points",
                                    "entrants": "10"
                                },
                                {
                                    "code": "T224",
                                    "description": "between 224 and 239 tariff points",
                                    "entrants": "0"
                                },
                                {
                                    "code": "T240",
                                    "description": "240 or more tariff points",
                                    "entrants": "0"
                                }
                            ],
                            "subject": {
                                "code": "CAH09-01-01",
                                "english_label": "Mathematics",
                                "welsh_label": "Mathemateg"
                            },
                            "unavailable": {
                                "code": 0,
                                "reason": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Mathematics."
                            }
                        }
                    ],
                    "leo": [
                        {
                            "aggregation_level": 23,
                            "higher_quartile": 21500,
                            "lower_quartile": 12000,
                            "median": 16000,
                            "number_of_graduates": 125,
                            "subject": {
                                "code": "CAH18-01-05",
                                "english_label": "Media studies",
                                "welsh_label": "Astudiaethau cyfryngau"
                            }
                        },
                        {
                            "aggregation_level": 23,
                            "higher_quartile": 21500,
                            "lower_quartile": 12000,
                            "median": 16000,
                            "number_of_graduates": 125,
                            "subject": {
                                "code": "CAH18-01-05",
                                "english_label": "Media studies",
                                "welsh_label": "Astudiaethau cyfryngau"
                            }
                        }
                    ],
                }
            }
        }

    @classmethod
    def get_successful_course_load_response(cls):
        response = Response()
        response.status_code = HTTPStatus.OK
        response._content = json.dumps(cls.get_successful_course_load_content()).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_course_load_response(cls):
        response = Response()
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        response._content = json.dumps(None).encode('utf-8')
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


class InstitutionMocks:
    @classmethod
    def get_successful_institution_load_content(cls):
        return {
            "_id": "5c59806500f91b809b8a6977",
            "created_at": "2019-05-06T00:00:00.0000000+00:00",
            "institution": {
                "apr_outcome": "Meets requirements",
                "contact_details": {
                    "address": {
                        "line_1": "Goldsmiths College",
                        "line_2": "8 Lewisham Way",
                        "line_3": "",
                        "line_4": "",
                        "town": "London",
                        "county": "England",
                        "post_code": "SE14 6NW"
                    },
                    "telephone": "020 7919 7171"
                },
                "courses": [
                    {
                        "distance_learning": {
                            "code": 0,
                            "label": "Course is available other than by distance learning"
                        },
                        "honours_award_provision": True,
                        "kis_course_id": "K1T67",
                        "kis_mode": {
                            "code": 1,
                            "label": "Full-time"
                        },
                        "links": {
                            "course_page": {
                                "english": "http://www.gold.ac.uk/ug/ba-anthropology-visual-practice/",
                                "welsh": ""
                            },
                            "self": ""
                        },
                        "locations": [
                            {
                                "name": {
                                    "english": "Goldsmiths College",
                                    "welsh": ""
                                }
                            }
                        ],
                        "qualification": {
                            "code": 0,
                            "label": "BA"
                        },
                        "sandwich_year": {
                            "code": 0,
                            "label": "Not available"
                        },
                        "title": {
                            "english": "Anthropology & Visual Practice",
                            "welsh": ""
                        },
                        "year_abroad": {
                            "code": 0,
                            "label": "Not available"
                        }
                    }
                ],
                "links": {
                    "institution_homepage": "http://www.gold.ac.uk",
                    "self": "",
                },
                "student_unions": [
                    {
                        "link": {
                            "english": "http://www.goldsmithssu.org/",
                            "welsh": ""
                        },
                        "name": {
                            "english": "Goldsmiths College",
                            "welsh": ""
                        }
                    },
                    {
                        "link": {
                            "english": "http://www.goldsmithssu.org/",
                            "welsh": ""
                        },
                        "name": {
                            "english": "GoldSmiths Test College",
                            "welsh": ""
                        }
                    }
                ],
                "pub_ukprn_country": {'code': 'XF', 'name': "England"},
                "pub_ukprn_name": "Goldsmiths, University of London",
                "pub_ukprn": 10002718,
                "tef_outcome": "Bronze",
                "total_number_of_courses": 30,
                "ukprn_country": "England",
                "ukprn_name": "Goldsmiths, University of London",
                "ukprn": 10002718
            },
            "version": 1
        }

    @classmethod
    def get_successful_institution_load_response(cls):
        response = Response()
        response.status_code = HTTPStatus.OK
        response._content = json.dumps(cls.get_successful_institution_load_content()).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_institution_load_response(cls):
        response = Response()
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        response._content = json.dumps(None).encode('utf-8')
        return response
