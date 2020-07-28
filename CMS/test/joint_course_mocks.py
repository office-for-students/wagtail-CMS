import json
from requests.models import Response
from http import HTTPStatus


class NewJointCourseFormatMocks:

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
                "accreditations": [
                    {
                        "type": "00601",
                        "accreditor_url": "http://www.accaglobal.com/en/qualifications/apply-now/exemptions.html",
                        "text": {
                            "english": "Accredited by the Association of Chartered Certified Accountants (ACCA) for the purpose of exemptions from some professional examinations.",
                            "welsh": "Achrededig gan Gymdeithas Cyfrifyddion Siartredig Ardystiedig (ACCA) at bwrpas eithriadau rhag rhai arholiadau proffesiynol."
                        },
                        "dependent_on": {
                            "code": 0,
                            "label": "Accreditation is not dependent on student choice"
                        }
                    },
                    {
                        "type": "00901",
                        "accreditor_url": "http://www.aacsb.edu/accreditation/accredited-members/global-listing",
                        "text": {
                            "english": "Accredited by the Association to Advance Collegiate Schools of Business (AACSB).",
                            "welsh": "Achrededig gan Gymdeithas Hyrwyddo Ysgolion Colegol Busnes (AACSB)"
                        },
                        "dependent_on": {
                            "code": 0,
                            "label": "Accreditation is not dependent on student choice"
                        }
                    },
                    {
                        "type": "07601",
                        "accreditor_url": "https://www.icas.com/education-and-qualifications/exam-exemptions-for-ca-qualification",
                        "text": {
                            "english": "Accredited by the Institute of Chartered Accountants Scotland (ICAS) for the purpose of exemption from some professional examinations.",
                            "welsh": "Achrededig gan Sefydliad Cyfrifwyr Siartredig yn yr Alban (ICAS) at bwrpas eithrio rhag rhai arholiadau proffesiynol."
                        },
                        "dependent_on": {
                            "code": 0,
                            "label": "Accreditation is not dependent on student choice"
                        }
                    },
                    {
                        "type": "07501",
                        "accreditor_url": "http://www.icaew.com/en/qualifications-and-programmes/aca/aca-training-in-the-uk/exams/credit-for-prior-learning",
                        "text": {
                            "english": "Accredited by the Institute of Chartered Accountants in England and Wales (ICAEW) for the purpose of exemption from some professional examinations.",
                            "welsh": "Achrededig gan Sefydliad Cyfrifwyr Siartredig yng Nghymru a Lloegr (ICAEW) at bwrpas eithrio rhag rhai arholiadau proffesiynol."
                        },
                        "dependent_on": {
                            "code": 0,
                            "label": "Accreditation is not dependent on student choice"
                        }
                    },
                    {
                        "type": "03701",
                        "accreditor_url": "https://www.cipfa.org/qualifications/exemptions",
                        "text": {
                            "english": "Accredited by the Chartered Institute of Public Finance and Accountancy (CIPFA) for the purpose of exemption from some professional examinations.",
                            "welsh": "Achrededig gan Sefydliad Siartredig Cyllid Cyhoeddus a Chyfrifyddiaeth (CIPFA) at bwrpas eithrio rhag rhai arholiadau proffesiynol."
                        },
                        "dependent_on": {
                            "code": 0,
                            "label": "Accreditation is not dependent on student choice"
                        }
                    },
                    {
                        "type": "03401",
                        "accreditor_url": "http://www.cimaglobal.com/Study-with-us/Exemptions/",
                        "text": {
                            "english": "Accredited by the Chartered Institute of Management Accountants (CIMA) for the purpose of exemption from some professional examinations through the Accredited degree accelerated route.",
                            "welsh": "Achrededig gan Sefydliad Siartredig Cyfrifwyr Rheolaeth (CIMA) at bwrpas eithrio rhag rhai arholiadau proffesiynol drwy lwybr carlam gradd Achrededig."
                        },
                        "dependent_on": {
                            "code": 0,
                            "label": "Accreditation is not dependent on student choice"
                        }
                    }
                ],
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
                        "code": "CAH09-01-01",
                        "level": 3,
                        "english": "Mathematics",
                        "welsh": "Mathemateg"
                    },
                    {
                        "code": "CAH17-01-04",
                        "level": 3,
                        "english": "Management studies",
                        "welsh": "Astudiaethau rheoli"
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
                        },
                        {
                          "aggregation_level": 13,
                          "number_of_students": 60,
                          "question_1": {
                            "description": "Staff are good at explaining things",
                            "agree_or_strongly_agree": 71
                          },
                          "question_2": {
                            "description": "Staff have made the subject interesting",
                            "agree_or_strongly_agree": 63
                          },
                          "question_3": {
                            "description": "The course is intellectually stimulating",
                            "agree_or_strongly_agree": 70
                          },
                          "question_4": {
                            "description": "My course has challenged me to achieve my best work",
                            "agree_or_strongly_agree": 77
                          },
                          "question_5": {
                            "description": "My course has provided me with opportunities to explore ideas or concepts in depth",
                            "agree_or_strongly_agree": 84
                          },
                          "question_6": {
                            "description": "My course has provided me with opportunities to bring information and ideas together from different topics",
                            "agree_or_strongly_agree": 70
                          },
                          "question_7": {
                            "description": "My course has provided me with opportunities to apply what I have learnt",
                            "agree_or_strongly_agree": 57
                          },
                          "question_8": {
                            "description": "The criteria used in marking have been clear in advance",
                            "agree_or_strongly_agree": 78
                          },
                          "question_9": {
                            "description": "Marking and assessment has been fair",
                            "agree_or_strongly_agree": 74
                          },
                          "question_10": {
                            "description": "Feedback on my work has been timely",
                            "agree_or_strongly_agree": 66
                          },
                          "question_11": {
                            "description": "I have received helpful comments on my work",
                            "agree_or_strongly_agree": 60
                          },
                          "question_12": {
                            "description": "I have been able to contact staff when I needed to",
                            "agree_or_strongly_agree": 84
                          },
                          "question_13": {
                            "description": "I have received sufficient advice and guidance in relation to my course",
                            "agree_or_strongly_agree": 76
                          },
                          "question_14": {
                            "description": "Good advice was available when I needed to make study choices on my course",
                            "agree_or_strongly_agree": 66
                          },
                          "question_15": {
                            "description": "The course is well organised and running smoothly",
                            "agree_or_strongly_agree": 69
                          },
                          "question_16": {
                            "description": "The timetable works efficiently for me",
                            "agree_or_strongly_agree": 88
                          },
                          "question_17": {
                            "description": "Any changes in the course or teaching have been communicated effectively",
                            "agree_or_strongly_agree": 75
                          },
                          "question_18": {
                            "description": "The IT resources and facilities provided have supported my learning well",
                            "agree_or_strongly_agree": 80
                          },
                          "question_19": {
                            "description": "The library resources (e.g. books, online services and learning spaces) have supported my learning well",
                            "agree_or_strongly_agree": 93
                          },
                          "question_20": {
                            "description": "I have been able to access course-specific resources (e.g. equipment, facilities, software, collections) when I needed to",
                            "agree_or_strongly_agree": 88
                          },
                          "question_21": {
                            "description": "I feel part of a community of staff and students",
                            "agree_or_strongly_agree": 59
                          },
                          "question_22": {
                            "description": "I have had the right opportunities to work with other students as part of my course",
                            "agree_or_strongly_agree": 87
                          },
                          "question_23": {
                            "description": "I have had the right opportunities to provide feedback on my course",
                            "agree_or_strongly_agree": 80
                          },
                          "question_24": {
                            "description": "Staff value students' views and opinions about the course",
                            "agree_or_strongly_agree": 70
                          },
                          "question_25": {
                            "description": "It is clear how students' feedback on the course has been acted on",
                            "agree_or_strongly_agree": 47
                          },
                          "question_26": {
                            "description": "The students' union (association or guild) effectively represents students' academic interests",
                            "agree_or_strongly_agree": 45
                          },
                          "question_27": {
                            "description": "Overall, I am satisfied with the quality of the course",
                            "agree_or_strongly_agree": 78
                          },
                          "response_rate": 66,
                          "subject": {
                            "code": "CAH17-01-04",
                            "english_label": "Management studies",
                            "welsh_label": "Astudiaethau rheoli"
                          },
                          "unavailable": {
                            "code": 0,
                            "reason_english": "There was not enough data to publish information specifically for this course. This is either because the course size is small or not enough students responded to a survey. For this reason, the data displayed is for all students in Management studies.",
                            "reason_welsh": "Nid oedd digon o ddata ar gael i gyhoeddi gwybodaeth yn benodol ar gyfer y cwrs hwn. Mae hyn naill ai oherwydd bod maint y cwrs yn fach neu am nad ymatebodd digon o fyfyrwyr i arolwg. Am y rheswm hwn, mae'r data a ddangosir ar gyfer yr holl fyfyrwyr mewn Astudiaethau rheoli."
                          }
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
