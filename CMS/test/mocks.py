import json
from requests.models import Response
from http import HTTPStatus


class NewCourseFormatMocks:

    @classmethod
    def get_successful_course_load_content(cls):
        return {
            "_id": "d450f6e6-940e-11ea-9481-0242ac100705",
            "created_at": "2020-05-12T05:10:00.075055",
            "version": 81,
            "partition_key": "81",
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
                "code": "XH",
                "name": "Scotland"
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
                "pub_ukprn_name": "University of Glasgow",
                "pub_ukprn_welsh_name": "University of Glasgow",
                "pub_ukprn": "10007794",
                "ukprn_name": "University of Glasgow",
                "ukprn_welsh_name": "University of Glasgow",
                "ukprn": "10007794"
              },
              "kis_course_id": "N400-2310",
              "apw_top_student_satisfaction": "76",
              "apw_top_average_salary": "37564",
              "apw_top_employment": "99",
              "length_of_course": {
                "code": 4,
                "label": "4 stages"
              },
              "links": {
                "assessment_method": {
                  "english": "https://www.gla.ac.uk/t4/progspecs/files/2018/BACC_ACCOUNTANCY_N400-2310_FINAL_PROGRAMME_SPECIFICATION_(2).pdf"
                },
                "course_cost": {
                  "english": "https://www.gla.ac.uk/undergraduate/degrees/accountancy/#tab=fees"
                },
                "course_page": {
                  "english": "http://www.gla.ac.uk/undergraduate/degrees/accountancy/"
                },
                "employment_details": {
                  "english": "http://www.gla.ac.uk/undergraduate/degrees/accountancy/"
                },
                "financial_support_details": {
                  "english": "http://www.gla.ac.uk/services/registry/finance/"
                },
                "learning_and_teaching_methods": {
                  "english": "http://senate.gla.ac.uk/progspecs/BAcc_Single_Hons.pdf"
                },
                "student_union": {
                  "english": "http://www.guu.co.uk"
                }
              },
              "locations": [
                {
                  "links": {
                    "accommodation": {
                      "english": "http://www.gla.ac.uk/undergraduate/accommodation/"
                    },
                    "student_union": {
                      "english": "http://www.src.gla.ac.uk/"
                    }
                  },
                  "latitude": "55.872",
                  "longitude": "-4.288",
                  "name": {
                    "english": "Glasgow Campus"
                  },
                  "ucas_course_id": "4669"
                }
              ],
              "mode": {
                "code": 1,
                "label": "Full-time"
              },
              "qualification": {
                "code": "001",
                "label": "BAcc",
                "level": "first-degree"
              },
              "sandwich_year": {
                "code": 0,
                "label": "Not available"
              },
              "subjects": [
                {
                  "code": "CAH17-01-08",
                  "level": 3,
                  "english": "Accounting",
                  "welsh": "Cyfrifeg"
                }
              ],
              "title": {
                "english": "Accountancy"
              },
              "ucas_programme_id": "A24-E28",
              "year_abroad": {
                "code": 1,
                "label": "Optional"
              },
              "statistics": {
                "continuation": [
                  {
                    "aggregation_level": 14,
                    "continuing_with_provider": 85,
                    "dormant": 10,
                    "gained": 0,
                    "left": 5,
                    "lower": 0,
                    "number_of_students": 20
                  }
                ],
                "employment": [
                  {
                    "aggregation_level": 24,
                    "assumed_to_be_unemployed": 5,
                    "in_study": 0,
                    "in_work": 80,
                    "in_work_and_study": 10,
                    "in_work_or_study": 95,
                    "not_available_for_work_or_study": 5,
                    "number_of_students": 35,
                    "response_rate": 75,
                    "unavailable": {
                      "code": 0,
                      "reason_english": "We have combined data for two years of this course, as there was not enough to publish the most recent year's data only.",
                      "reason_welsh": "Rydym wedi cyfuno data ar gyfer dwy flynedd o'r cwrs hwn gan nad oedd digon ar gael i gyhoeddi data'r flwyddyn ddiweddaraf yn unig."
                    }
                  }
                ],
                "entry": [
                  {
                    "a-level": 65,
                    "access": 15,
                    "aggregation_level": 14,
                    "another_higher_education_qualifications": 15,
                    "baccalaureate": 0,
                    "degree": 0,
                    "foundation": 0,
                    "none": 0,
                    "number_of_students": 10,
                    "other_qualifications": 0
                  }
                ],
                "job_type": [
                  {
                    "aggregation_level": 24,
                    "non_professional_or_managerial_jobs": 10,
                    "number_of_students": 25,
                    "professional_or_managerial_jobs": 90,
                    "response_rate": 75,
                    "unavailable": {
                      "code": 0,
                      "reason_english": "We have combined data for two years of this course, as there was not enough to publish the most recent year's data only.",
                      "reason_welsh": "Rydym wedi cyfuno data ar gyfer dwy flynedd o'r cwrs hwn gan nad oedd digon ar gael i gyhoeddi data'r flwyddyn ddiweddaraf yn unig."
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
                        "order": "1"
                      },
                      {
                        "job": "Managers, directors and senior officials",
                        "percentage_of_students": "10",
                        "order": "2"
                      },
                      {
                        "job": "Information technology and telecommunications professionals",
                        "percentage_of_students": "5",
                        "order": "3"
                      },
                      {
                        "job": "Artistic, literary and media occupations",
                        "percentage_of_students": "5",
                        "order": "4"
                      },
                      {
                        "job": "Business and public service associate professionals",
                        "percentage_of_students": "5",
                        "order": "5"
                      },
                      {
                        "job": "Skilled trades occupations",
                        "percentage_of_students": "5",
                        "order": "6"
                      },
                      {
                        "job": "Sales occupations",
                        "percentage_of_students": "5",
                        "order": "7"
                      },
                      {
                        "job": "Customer service occupations",
                        "percentage_of_students": "5",
                        "order": "8"
                      }
                    ],
                    "number_of_students": 25,
                    "response_rate": 75,
                    "unavailable": {
                      "code": 0,
                      "reason_english": "We have combined data for two years of this course, as there was not enough to publish the most recent year's data only.",
                      "reason_welsh": "Rydym wedi cyfuno data ar gyfer dwy flynedd o'r cwrs hwn gan nad oedd digon ar gael i gyhoeddi data'r flwyddyn ddiweddaraf yn unig."
                    }
                  }
                ],
                "leo": [
                  {
                    "unavailable": {
                      "code": 1,
                      "reason_english": "We only have this data for English universities and colleges. This is because of differences in either policy or legislation relating to this data in the other countries of the UK. ",
                      "reason_welsh": "Mae ond gennym y data hwn ar gyfer prifysgolion a cholegau yn Lloegr. Mae hyn oherwydd gwahaniaethau mewn naill ai polisÂau neu ddeddfwriaeth sy'n ymwneud Â'r data hwn yng ngwledydd eraill y DU. ",
                      "find_out_more_english": "Find out more",
                      "find_out_more_welsh": "Cewch ragor o wybodaeth",
                      "url_english": "/about-our-data",
                      "url_welsh": "/cy/ynglŷn-ân-data-about-our-data-cy"
                    }
                  }
                ],
                "nss": [
                  {
                    "aggregation_level": 14,
                    "number_of_students": 20,
                    "question_1": {
                      "description": "Staff are good at explaining things",
                      "agree_or_strongly_agree": 90
                    },
                    "question_2": {
                      "description": "Staff have made the subject interesting",
                      "agree_or_strongly_agree": 80
                    },
                    "question_3": {
                      "description": "The course is intellectually stimulating",
                      "agree_or_strongly_agree": 70
                    },
                    "question_4": {
                      "description": "My course has challenged me to achieve my best work",
                      "agree_or_strongly_agree": 75
                    },
                    "question_5": {
                      "description": "My course has provided me with opportunities to explore ideas or concepts in depth",
                      "agree_or_strongly_agree": 80
                    },
                    "question_6": {
                      "description": "My course has provided me with opportunities to bring information and ideas together from different topics",
                      "agree_or_strongly_agree": 80
                    },
                    "question_7": {
                      "description": "My course has provided me with opportunities to apply what I have learnt",
                      "agree_or_strongly_agree": 45
                    },
                    "question_8": {
                      "description": "The criteria used in marking have been clear in advance",
                      "agree_or_strongly_agree": 55
                    },
                    "question_9": {
                      "description": "Marking and assessment has been fair",
                      "agree_or_strongly_agree": 75
                    },
                    "question_10": {
                      "description": "Feedback on my work has been timely",
                      "agree_or_strongly_agree": 70
                    },
                    "question_11": {
                      "description": "I have received helpful comments on my work",
                      "agree_or_strongly_agree": 60
                    },
                    "question_12": {
                      "description": "I have been able to contact staff when I needed to",
                      "agree_or_strongly_agree": 95
                    },
                    "question_13": {
                      "description": "I have received sufficient advice and guidance in relation to my course",
                      "agree_or_strongly_agree": 70
                    },
                    "question_14": {
                      "description": "Good advice was available when I needed to make study choices on my course",
                      "agree_or_strongly_agree": 50
                    },
                    "question_15": {
                      "description": "The course is well organised and running smoothly",
                      "agree_or_strongly_agree": 85
                    },
                    "question_16": {
                      "description": "The timetable works efficiently for me",
                      "agree_or_strongly_agree": 80
                    },
                    "question_17": {
                      "description": "Any changes in the course or teaching have been communicated effectively",
                      "agree_or_strongly_agree": 80
                    },
                    "question_18": {
                      "description": "The IT resources and facilities provided have supported my learning well",
                      "agree_or_strongly_agree": 75
                    },
                    "question_19": {
                      "description": "The library resources (e.g. books, online services and learning spaces) have supported my learning well",
                      "agree_or_strongly_agree": 95
                    },
                    "question_20": {
                      "description": "I have been able to access course-specific resources (e.g. equipment, facilities, software, collections) when I needed to",
                      "agree_or_strongly_agree": 95
                    },
                    "question_21": {
                      "description": "I feel part of a community of staff and students",
                      "agree_or_strongly_agree": 70
                    },
                    "question_22": {
                      "description": "I have had the right opportunities to work with other students as part of my course",
                      "agree_or_strongly_agree": 90
                    },
                    "question_23": {
                      "description": "I have had the right opportunities to provide feedback on my course",
                      "agree_or_strongly_agree": 90
                    },
                    "question_24": {
                      "description": "Staff value students' views and opinions about the course",
                      "agree_or_strongly_agree": 70
                    },
                    "question_25": {
                      "description": "It is clear how students' feedback on the course has been acted on",
                      "agree_or_strongly_agree": 50
                    },
                    "question_26": {
                      "description": "The students' union (association or guild) effectively represents students' academic interests",
                      "agree_or_strongly_agree": 58
                    },
                    "question_27": {
                      "description": "Overall, I am satisfied with the quality of the course",
                      "agree_or_strongly_agree": 90
                    },
                    "response_rate": 95
                  }
                ],
                "salary": [
                  {
                    "aggregation_level": 24,
                    "higher_quartile": 21000,
                    "lower_quartile": 16000,
                    "median": 20000,
                    "number_of_graduates": 20,
                    "response_rate": 85,
                    "sector_higher_quartile": 22000,
                    "sector_lower_quartile": 18000,
                    "sector_median": 20000,
                    "unavailable": {
                      "code": 0,
                      "reason_english": "We have combined data for two years of this course, as there was not enough to publish the most recent year's data only.",
                      "reason_welsh": "Rydym wedi cyfuno data ar gyfer dwy flynedd o'r cwrs hwn gan nad oedd digon ar gael i gyhoeddi data'r flwyddyn ddiweddaraf yn unig."
                    }
                  }
                ],
                "tariff": [
                  {
                    "aggregation_level": 24,
                    "number_of_students": 25,
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
                        "entrants": 0
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
                        "entrants": 0
                      },
                      {
                        "code": "T128",
                        "description": "between 128 and 143 tariff points",
                        "entrants": 0
                      },
                      {
                        "code": "T144",
                        "description": "between 144 and 159 tariff points",
                        "entrants": 5
                      },
                      {
                        "code": "T160",
                        "description": "between 160 and 175 tariff points",
                        "entrants": 10
                      },
                      {
                        "code": "T176",
                        "description": "between 176 and 191 tariff points",
                        "entrants": 10
                      },
                      {
                        "code": "T192",
                        "description": "between 192 and 207 tariff points",
                        "entrants": 5
                      },
                      {
                        "code": "T208",
                        "description": "between 208 and 223 tariff points",
                        "entrants": 10
                      },
                      {
                        "code": "T224",
                        "description": "between 224 and 239 tariff points",
                        "entrants": 30
                      },
                      {
                        "code": "T240",
                        "description": "240 or more tariff points",
                        "entrants": 30
                      }
                    ],
                    "unavailable": {
                      "code": 0,
                      "reason_english": "We have combined data for two years of this course, as there was not enough to publish the most recent year's data only.",
                      "reason_welsh": "Rydym wedi cyfuno data ar gyfer dwy flynedd o'r cwrs hwn gan nad oedd digon ar gael i gyhoeddi data'r flwyddyn ddiweddaraf yn unig."
                    }
                  }
                ]
              }
            },
            "id": "e24f738d-6431-1093-39a8-936e7edf0778"
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
