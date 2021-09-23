# Use this to access DICT/OPTIONS, don't access them directly
import re
import string


def cleanup_key(key):
    exclude = set(string.punctuation) - {'_', '-'}
    new = ''.join(ch for ch in key if ch not in exclude)
    new = re.sub('\s|[-]', '_', new)
    return new.lower()


def term_for_key(key: str, language: str) -> str:
    """ Method to use to access welsh translations for static content
        returns: a language specific translation or the origin key string passed in if it can't be found.
    """
    key = cleanup_key(key)
    term = DICT.get(key).get(language) if key in DICT else None
    if not term:
        term = STATISTICS.get(key).get(language) if key in STATISTICS else None
    if not term:
        term = UNAVAILABLE.get(key).get(language) if key in UNAVAILABLE else None
    if not term:
        term = JOBS.get(key).get(language) if key in JOBS else None
    if not term:
        term = OPTIONALS.get(key).get(language) if key in OPTIONALS else None
    if not term:
        term = DICT.get(key).get(language) if key in DICT else key
    return term


STATISTICS = {
    "academic_support": {
        "cy": "Cefnogaeth academaidd",
        "en": "Academic support"
    },
    "after_15_months": {
        "cy": "Ar ôl 15 mis",
        "en": "After 15 months"
    },
    "after_3_years": {
        "cy": "Ar ôl 3 blynedd",
        "en": "After 3 years"
    },
    "after_5_years": {
        "cy": "Ar ôl 5 blynedd",
        "en": "After 5 years"
    },
    "after_one_year": {
        "cy": "Ar ôl blwyddyn o astudio",
        "en": "After 1 year on the course"
    },
    "after_one_year_guidance": {
        "cy": "Bydd nifer y myfyrwyr yn dynodi maint y cwrs, ac os ceir mwy o bobl mae \n            hynny'n golygu ei fod yn fwy tebygol o gynrychioli canlyniadau myfyrwyr.",
        "en": "The number of students indicates the size of the course, and more people \n            means it is more likely to be representative of outcomes for students."
    },
    "assessment_and_feedback": {
        "cy": "Asesiad ac adborth",
        "en": "Assessment and feedback"
    },
    "data_from_people": {
        "cy": "Data gan (# o fyfyrwyr)",
        "en": "Data from (# of people)"
    },
    "earnings_after_the_course": {
        "cy": "Enillion ar ôl y cwrs",
        "en": "Earnings after the course"
    },
    "earnings_guidance_0": {
        "cy": "Mae rhywfaint o ddata gan raddedigion a arolygwyd yn ystod y pandemig COVID-19.",
        "en": "Some data is from graduates surveyed during the Covid-19 pandemic."
    },
    "earnings_guidance_1": {
        "cy": "mae marchnadoedd llaffur yn newid",
        "en": "Labour markets change"
    },
    "earnings_guidance_2": {
        "cy": "mae cyflogau'n amrywio yng ngwahanol rannau o'r DU",
        "en": "Salaries vary across regions in the UK"
    },
    "earnings_guidance_3": {
        "cy": "mae llawer o ffactorau'n effeithio ar enillion graddedigion",
        "en": "There are lots of factors that affect graduates' earnings"
    },
    "earnings_link": {
        "cy": "https://www.discoveruni.gov.uk/cy/how-choose-course-cy/rhagolygon-cyflogaeth-employment-prospects/",
        "en": "https://www.discoveruni.gov.uk/how-do-i-choose-course/employment-prospects/"
    },
    "employed_in_professional": {
        "cy": "Canran y rhai a gyflogir sydd mewn swydd broffesiynol neu swydd reoli ar ôl gorffen y cwrs.",
        "en": "Employed in a professional or managerial job"
    },
    "employed_not_in_professional": {
        "cy": "Canran y rhai a gyflogir nad ydynt mewn swydd broffesiynol neu swydd reoli ar gorffen y cwrs.",
        "en": "Employed not in a professional or managerial job"
    },
    "employment_15_months": {
        "cy": "Cyflogaeth 15 mis ar ôl y cwrs",
        "en": "Employment 15 months after the course"
    },
    "employment_after_the_course": {
        "cy": "Yr hyn y mae graddedigion yn ei wneud 15 mis ar y cwrs",
        "en": "What graduates are doing 15 months after the course"
    },
    "employment_guidance_1": {
        "cy": "Daw rhywfaint o ddata gan raddedigion a gymerodd ran yn yr arolwg yn ystod y pandemig.",
        "en": "Some data is from graduates surveyed during the pandemic"
    },
    "employment_guidance_2": {
        "cy": "Bydd marchnadoedd llafur yn amrywio ac yn newid dros amser",
        "en": "Labour markets vary and change over time"
    },
    "employment_guidance_3": {
        "cy": "Bydd cyfleoedd am gyflogaeth a swyddi'n amrywio ar draws rhanbarthau'r DU",
        "en": "Employment and job opportunities vary across regions in the UK"
    },
    "employment_link": {
        "cy": "https://www.discoveruni.gov.uk/cy/how-choose-course-cy/rhagolygon-cyflogaeth-employment-prospects/",
        "en": "https://www.discoveruni.gov.uk/how-do-i-choose-course/employment-prospects/"
    },
    "entry_guidance": {
        "cy": "Dyma'r cymwysterau a oedd gan fyfywyr wrth gael eu derbyn ar y cwrs yma. Nid rhestr o gymwysterau sydd eu hangen ar rywun er mwyn cael eu derbyn ar y cwrs yw hon",
        "en": "These are the qualifications students had when they were accepted onto this course. This is not a list of qualifications a person needs to have to be accepted onto this course"
    },
    "entry_information": {
        "cy": "Gwybodaeth am fynediad",
        "en": "Entry Information"
    },
    "future": {
        "cy": "Y Dyfodol",
        "en": "Future"
    },
    "future_subtitle": {
        "cy": "Mae fy ngwaith presennol yn cyd-fynd â'm cynlluniau ar gyfer y dyfodol.",
        "en": " My current work fits with my future plans."
    },
    "graduate_guidance_1": {
        "cy": "Nifer y bobl y mae'r data'n seiliedig arnynt - bydd mwy o bobl yn golygu ei bod hi'n debygol y ceir darlun cliriach o brofiadau myfyrwyr. Dylech hefyd ystyried canran y myfyrwyr a ymatebodd i'r arolwg.",
        "en": "Number of people the data is based on - more people mean it is more likely giving a clearer picture of student experience. Also consider the percentage of graduates who responded to the survey."
    },
    "graduate_guidance_2": {
        "cy": "Gall rhywfaint o ddata fod ar gyfer cwrs a rhywfaint ar gyfer pwnc - mae data cwrs yn fwy penodol ond bydd data pwnc yn dal i roi syniad o farn myfyrwyr. Byddwch yn ofalus wrth gymharu'r naill a'r llall.",
        "en": "Some data may be for a course and some for a subject - course data is more specific but subject data will still give an indication of students’ views. Use caution when comparing the two."
    },
    "graduate_link": {
        "cy": "https://discoveruni.gov.uk/cy/yngl%C5%B7n-%C3%A2n-data-about-our-data-cy/#arolwg_canlyniadau_graddedigion",
        "en": "https://www.discoveruni.gov.uk/about-our-data/#graduate_outcomes_survey"
    },
    "graduate_perceptions": {
        "cy": "Canfyddiadau graddedigion",
        "en": "Graduate perceptions"
    },
    "information_on_uni": {
        "cy": "Gwybodaeth ar wefan y prifysgol",
        "en": "Information on the uni website"
    },
    "learning_community": {
        "cy": "Cymuned ddysgu",
        "en": "Learning community"
    },
    "learning_opportunities": {
        "cy": "Cyfleoedd dysgu",
        "en": "Learning opportunities"
    },
    "learning_resources": {
        "cy": "Adnoddau dysgu",
        "en": "Learning resources"
    },
    "meaningfulness": {
        "cy": "Pa mor ystyrlon",
        "en": "Meaningfulness"
    },
    "meaningfulness_subtitle": {
        "cy": "Mae fy ngwaith presennol yn ystyrlon.",
        "en": "My current work is meaningful."
    },
    "national_average": {
        "cy": "Cyfartaledd cenedlaethol",
        "en": "National average"
    },
    "no_data_available": {
        "cy": "Nid yw'r data ar gael",
        "en": "No data available"
    },
    "nss_question_1": {
        "cy": "Mae'r staff yn dda am esbonio pethau",
        "en": "Staff are good at explaining things"
    },
    "nss_question_10": {
        "cy": "Mae’r adborth ar fy ngwaith i wedi bod yn amserol",
        "en": "Feedback on my work has been timely."
    },
    "nss_question_11": {
        "cy": "Rydw i wedi cael sylwadau defnyddiol ar fy ngwaith",
        "en": "I have received helpful comments on my work."
    },
    "nss_question_12": {
        "cy": "Rydw i wedi gallu cysylltu â staff pan oeddwn i angen gwneud hynny",
        "en": "I have been able to contact staff when I needed to."
    },
    "nss_question_13": {
        "cy": "Rydw i wedi cael digon o gyngor ac arweiniad mewn perthynas â'm cwrs",
        "en": "I have received sufficient advice and guidance in relation to my course."
    },
    "nss_question_14": {
        "cy": "Roedd cyngor da ar gael i mi pan oeddwn i eisiau gwneud dewisiadau astudio ar fy nghwrs",
        "en": "Good advice was available when I needed to make study choices on my course."
    },
    "nss_question_15": {
        "cy": "Mae'r cwrs wedi’i drefnu'n dda ac mae'n rhedeg yn hwylus",
        "en": "The course is well organised and is running smoothly."
    },
    "nss_question_16": {
        "cy": "Mae’r amserlen yn gweithio’n effeithlon i mi",
        "en": "The timetable works efficiently for me."
    },
    "nss_question_17": {
        "cy": "Cafwyd cyfathrebu effeithiol ynghylch unrhyw newidiadau o ran y cwrs neu'r addysgu",
        "en": "Any changes in the course or teaching have been communicated effectively."
    },
    "nss_question_18": {
        "cy": "Mae’r adnoddau a’r cyfleusterau TG sydd wedi’u darparu wedi cefnogi fy nysgu i’n dda",
        "en": "The IT resources and facilities provided have supported my learning well."
    },
    "nss_question_19": {
        "cy": "Mae’r adnoddau llyfrgell (e.e. llyfrau, gwasanaethau ar-lein a gofod dysgu) wedi cefnogi fy nysgu i’n dda",
        "en": "The library resources (e.g. books, online services and learning spaces) have supported my learning well."
    },
    "nss_question_2": {
        "cy": "Mae'r staff wedi gwneud y pwnc yn ddiddorol",
        "en": "Staff have made the subject interesting."
    },
    "nss_question_20": {
        "cy": "Rydw i wedi gallu cael mynediad at adnoddau penodol i gwrs (e.e. offer, cyfleusterau, meddalwedd, casgliadau) pan oedd angen i mi wneud hynny",
        "en": "I have been able to access course-specific resources (e.g. equipment, facilities, software, collections) when I needed to."
    },
    "nss_question_21": {
        "cy": "Rydw i’n teimlo’n rhan o gymuned o staff a myfyrwyr",
        "en": "I feel part of a community of staff and students."
    },
    "nss_question_22": {
        "cy": "Rydw i wedi cael cyfleoedd priodol i weithio gyda myfyrwyr eraill fel rhan o'm cwrs",
        "en": "I have had the right opportunities to work with other students as part of my course."
    },
    "nss_question_23": {
        "cy": "Rydw i wedi cael cyfleoedd priodol i roi adborth ar fy nghwrs",
        "en": "I have had the right opportunities to provide feedback on my course."
    },
    "nss_question_24": {
        "cy": "Mae’r staff yn gwerthfawrogi barn a safbwynt y myfyrwyr am y cwrs",
        "en": "Staff value students’ views and opinions about the course."
    },
    "nss_question_25": {
        "cy": "Mae’n glir sut gweithredwyd fel ymateb i adborth y myfyrwyr ar y cwrs",
        "en": "It is clear how students’ feedback on the course has been acted on."
    },
    "nss_question_26": {
        "cy": "Mae undeb y myfyrwyr (cymdeithas neu urdd) yn cynrychioli buddiannau academaidd y myfyrwyr yn effeithiol",
        "en": "The students’ union (association or guild) effectively represents students’ academic interests."
    },
    "nss_question_3": {
        "cy": "Mae'r cwrs yn symbylu'r deallusrwydd",
        "en": "The course is intellectually stimulating."
    },
    "nss_question_4": {
        "cy": "Mae fy nghwrs wedi fy herio i i wneud fy ngwaith gorau",
        "en": "My course has challenged me to achieve my best work."
    },
    "nss_question_5": {
        "cy": "Mae fy nghwrs wedi rhoi cyfleoedd i mi i archwilio syniadau neu gysyniadau’n fanwl",
        "en": "My course has provided me with opportunities to explore ideas or concepts in depth."
    },
    "nss_question_6": {
        "cy": "Mae fy nghwrs wedi rhoi cyfleoedd i mi i ddod â gwybodaeth a syniadau at ei gilydd o wahanol bynciau",
        "en": "My course has provided me with opportunities to bring information and ideas together from different topics."
    },
    "nss_question_7": {
        "cy": "Mae fy nghwrs wedi rhoi cyfleoedd i mi i ddefnyddio’r hyn rydw i wedi’i ddysgu",
        "en": "My course has provided me with opportunities to apply what I have learnt."
    },
    "nss_question_8": {
        "cy": "Mae'r meini prawf a ddefnyddir ar gyfer marcio wedi cael eu gwneud yn eglur ymlaen llaw",
        "en": "The criteria used in marking have been clear in advance."
    },
    "nss_question_9": {
        "cy": "Mae’r marcio a’r asesu wedi bod yn deg",
        "en": "Marking and assessment has been fair."
    },
    "occupation_type": {
        "cy": "Mathau o swydd 15 mis ar ôl y cwrs",
        "en": "Occupation types 15 months after the course"
    },
    "organisation_and_management": {
        "cy": "Trefniant a rheolaeth",
        "en": "Organisation and management"
    },
    "overall_satisfied": {
        "cy": "Rwy’n fodlon ag ansawdd y cwrs ar y cyfan",
        "en": "Overall I am satisfied with the quality of the course"
    },
    "percent_of_those_asked": {
        "cy": "% o'r rhai y gofynnwyd iddynt",
        "en": "% of those asked"
    },
    "read_more_about_continuation": {
        "cy": "Darllenwch fwy am Parhad",
        "en": "Read more about Continuation"
    },
    "read_more_about_earnings": {
        "cy": "Darllen mwy am enillion",
        "en": "Read more about earnings"
    },
    "read_more_about_employment": {
        "cy": "Darllen mwy am gyflogaeth",
        "en": "Read more about employment"
    },
    "read_more_about_entry": {
        "cy": "Darllen mwy am ddata mynediad",
        "en": "Read more about entry data"
    },
    "read_more_about_graduate_perceptions": {
        "cy": "Darllenwch fwy am Canfyddiadau Graddedigion",
        "en": "Read more about Graduate Perceptions"
    },
    "read_more_about_satisfaction": {
        "cy": "Darllenwch fwy am Arolwg Cenedlaethol o Fyfyrwyr",
        "en": "Read more about the National Student Survey"
    },
    "read_more_about_this_data": {
        "cy": "Darllenwch ragor am y data hwn. ",
        "en": "Read more about this data"
    },
    "satisfaction_guidance_1": {
        "cy": "<strong>Nifer y bobl y mae'r data'n seiliedig arnynt</strong> - \n            bydd mwy o bobl yn golygu ei bod hi'n debygol y ceir darlun cliriach o brofiadau myfyrwyr. \n            Dylech hefyd ystyried canran y myfyrwyr a ymatebodd i'r arolwg.",
        "en": "<strong>Number of people the data is based on</strong> - \n            more people mean it is more likely giving a clearer picture of student experience. \n            Also consider the percentage of students who responded to the survey."
    },
    "satisfaction_guidance_2": {
        "cy": "<strong>Gall rhywfaint o ddata fod ar gyfer cwrs a rhywfaint ar gyfer pwnc</strong> - \n            mae data cwrs yn fwy penodol ond bydd data pwnc yn dal i roi syniad o farn myfyrwyr. \n            Byddwch yn ofalus wrth gymharu'r naill a'r llall. \n            Darllenwch fwy am Arolwg Cenedlaethol o Fyfyrwyr",
        "en": "<strong>Some data may be for a course and some for a subject</strong> -\n            course data is more specific but subject data will still give an indication of students’ views. \n            Use caution when comparing the two."
    },
    "student_voice": {
        "cy": "Llais y myfyriwr",
        "en": "Student voice"
    },
    "teaching_on_my_course": {
        "cy": "Yr addysgu ar fy nghwrs",
        "en": "Teaching on my course"
    },
    "ucas_tariff_points": {
        "cy": "Pwyntiau Tariff UCAS",
        "en": "UCAS Tariff points"
    },
    "unavailable_data_message": {
        "cy": "Gall hyn fod oherwydd bod maint y cwrs yn rhy fach. Nid yw hyn yn adlewyrchu ansawdd y cwrs.",
        "en": "This may be because the course size is too small or not enough students responded to the survey. This does not reflect on the quality of the course."
    },
    "usefulness": {
        "cy": "Pa mor ddefnyddiol",
        "en": "Usefulness"
    },
    "usefulness_subtitle": {
        "cy": "Rwy'n defnyddio'r hyn a ddysgais wrth astudio yn fy ngwaith presennol.",
        "en": "I am utilising what I learnt during my studies in my current work."
    }
}

UNAVAILABLE = {
    "data_displayed": {
        "cy": "Daw'r data a ddangosir gan fyfyrwyr ymlaen",
        "en": "The data displayed is from students on"
    },
    "message_1": {
        "cy": "Daw'r data a ddangosir gan fyfyrwyr ar y cwrs hwn a chyrsiau <b>{}</b> eraill. Nid oedd digon o ddata i gyhoeddi gwybodaeth yn benodol ar gyfer y cwrs hwn. Gall hyn fod oherwydd bod maint y cwrs yn rhy fach. Nid yw hyn yn adlewyrchu ansawdd y cwrs.",
        "en": "The data displayed is from students on this and other courses in <b>{}</b>. There was not enough data to publish information specifically for this course. This may be because the course size is too small. This does not reflect on the quality of the course."
    },
    "message_10": {
        "cy": "Mae hyn oherwydd nad yw'r cwrs wedi'i gynnal eto neu nid yw wedi cael ei gynnal yn ddigon hir i’r data hwn fod ar gael. Nid yw hyn yn adlewyrchu ansawdd y cwrs.",
        "en": "This is because the course has not yet run or has not been running long enough for this data to be available. This does not reflect on the quality of the course."
    },
    "message_10_header": {
        "cy": "Nid yw'r data ar gael.",
        "en": "No data available."
    },
    "message_11": {
        "cy": "Nid yw hyn yn adlewyrchu ansawdd y cwrs.",
        "en": "This does not reflect on the quality of the course."
    },
    "message_11_header": {
        "cy": "Nid yw'r data ar gael.",
        "en": "No data available."
    },
    "message_1_header": {
        "cy": "Hwn a chyrsiau eraill.",
        "en": "This and other courses."
    },
    "message_2": {
        "cy": "Gall hyn fod oherwydd bod maint y cwrs yn rhy fach. Nid yw hyn yn adlewyrchu ansawdd y cwrs.",
        "en": "This may be because the course size is too small. This does not reflect on the quality of the course."
    },
    "message_2_header": {
        "cy": "Daw'r data a ddangosir gan fyfyrwyr yn ystod y ddwy flynedd flaenorol.",
        "en": "This course over 2 years."
    },
    "message_3": {
        "cy": "Daw'r data a ddangosir gan fyfyrwyr ar y cwrs hwn a chyrsiau <b>{}</b> eraill yn ystod y ddwy flynedd flaenorol. Nid oedd digon o ddata i gyhoeddi gwybodaeth yn benodol ar gyfer y cwrs hwn. Gall hyn fod oherwydd bod maint y cwrs yn rhy fach. Nid yw hyn yn adlewyrchu ansawdd y cwrs.",
        "en": "The data displayed is from students on this and other courses over two years in <b>{}</b>. There was not enough data to publish information specifically for this course. This may be because the course size is too small. This does not reflect on the quality of the course."
    },
    "message_3_header": {
        "cy": "Cwrs hwn a chyrsiau eraill dros 2 flynedd.",
        "en": "This and other courses over 2 years."
    },
    "message_4": {
        "cy": "Daw'r data a ddangosir gan fyfyrwyr ar y cwrs hwn a chyrsiau <b>{}</b> eraill. Nid oedd digon o ddata i gyhoeddi gwybodaeth yn benodol ar gyfer y cwrs hwn. Gall hyn fod oherwydd bod maint y cwrs yn rhy fach neu nad oedd digon o fyfyrwyr wedi ymateb i'r arolwg. Nid yw hyn yn adlewyrchu ansawdd y cwrs.",
        "en": "The data displayed is from students on this and other courses in <b>{}</b>. There was not enough data to publish information specifically for this course. This may be because the course size is too small or not enough students responded to the survey. This does not reflect on the quality of the course."
    },
    "message_4_header": {
        "cy": "Hwn a chyrsiau eraill.",
        "en": "This and other courses."
    },
    "message_5": {
        "cy": "Gall hyn fod oherwydd bod maint y cwrs yn rhy fach neu nad oedd digon o fyfyrwyr wedi ymateb i'r arolwg. Nid yw hyn yn adlewyrchu ansawdd y cwrs.",
        "en": "This may be because the course size is too small or not enough students responded to the survey. This does not reflect on the quality of the course."
    },
    "message_5_header": {
        "cy": "Daw'r data a ddangosir gan fyfyrwyr yn ystod y ddwy flynedd flaenorol.",
        "en": "This course over 2 years."
    },
    "message_6": {
        "cy": "Daw'r data a ddangosir gan fyfyrwyr ar y cwrs hwn a chyrsiau <b>{}</b> eraill yn ystod y ddwy flynedd flaenorol. Nid oedd digon o ddata i gyhoeddi gwybodaeth yn benodol ar gyfer y cwrs hwn. Gall hyn fod oherwydd bod maint y cwrs yn rhy fach neu nad oedd digon o fyfyrwyr wedi ymateb i'r arolwg. Nid yw hyn yn adlewyrchu ansawdd y cwrs.",
        "en": "The data displayed is from students on this and other courses over two years in <b>{}</b>. There was not enough data to publish information specifically for this course. This may be because the course size is too small or not enough students responded to the survey. This does not reflect on the quality of the course."
    },
    "message_6_header": {
        "cy": "Cwrs hwn a chyrsiau eraill dros 2 flynedd.",
        "en": "This and other courses over 2 years."
    },
    "message_7": {
        "cy": "Gall hyn fod oherwydd bod maint y cwrs yn rhy fach. Nid yw hyn yn adlewyrchu ansawdd y cwrs.",
        "en": "This may be because the course size is too small. This does not reflect on the quality of the course."
    },
    "message_7_header": {
        "cy": "Nid yw'r data ar gael.",
        "en": "No data available."
    },
    "message_8": {
        "cy": "Daw'r data a ddangosir gan fyfyrwyr ar y cwrs hwn a chyrsiau <b>{}</b> eraill. Nid oedd digon o ddata i gyhoeddi gwybodaeth yn benodol ar gyfer y cwrs hwn. Mae hyn oherwydd nad yw'r cwrs wedi'i gynnal eto neu nid yw wedi cael ei gynnal yn ddigon hir i’r data hwn fod ar gael.",
        "en": "The data displayed is from students on this and other courses in <b>{}</b>. There was not enough data to publish information specifically for this course. This is because the course has not yet run or has not been running long enough for this data to be available."
    },
    "message_8_header": {
        "cy": "Hwn a chyrsiau eraill.",
        "en": "This and other courses."
    },
    "message_9": {
        "cy": "Daw'r data a ddangosir gan fyfyrwyr ar y cwrs hwn a chyrsiau <b>{}</b> eraill yn ystod y ddwy flynedd flaenorol. Nid oedd digon o ddata i gyhoeddi gwybodaeth yn benodol ar gyfer y cwrs hwn. Mae hyn oherwydd nad yw'r cwrs wedi'i gynnal eto neu nid yw wedi cael ei gynnal yn ddigon hir i’r data hwn fod ar gael.",
        "en": "The data displayed is from students on this and other courses over two years in <b>{}</b>. There was not enough data to publish information specifically for this course. This is because the course has not yet run or has not been running long enough for this data to be available."
    },
    "message_9_header": {
        "cy": "Cwrs hwn a chyrsiau eraill dros 2 flynedd.",
        "en": "This and other courses over 2 years."
    },
    "this_course": {
        "cy": "Y cwrs hwn",
        "en": "This course"
    }
}

JOBS = {
    "administrative_occupations": {
        "cy": "Galwedigaethau gweinyddol",
        "en": "Administrative occupations"
    },
    "administrative_occupations_communications": {
        "cy": "Galwedigaethau gweinyddol: Cyfathrebu",
        "en": "Administrative occupations: Communications"
    },
    "administrative_occupations_finance": {
        "cy": "Galwedigaethau gweinyddol: Cyllid",
        "en": "Administrative occupations: Finance"
    },
    "administrative_occupations_general": {
        "cy": "Galwedigaethau gweinyddol: Cyffredinol",
        "en": "Administrative occupations: General"
    },
    "administrative_occupations_government_and_related_organisations": {
        "cy": "Galwedigaethau gweinyddol: Llywodraeth a sefydliadau cysylltiedig",
        "en": "Administrative occupations: Government and related organisations"
    },
    "administrative_occupations_records": {
        "cy": "Galwedigaethau gweinyddol: Cofnodion",
        "en": "Administrative occupations: Records"
    },
    "animal_care_and_control_services": {
        "cy": "Gwasanaethau Gofal a Rheoli Anifeiliaid",
        "en": "Animal care and control services"
    },
    "architects_chartered_architectural_technologists_planning_officers_surveyors_and_construction_professionals": {
        "cy": "Penseiri, Technolegwyr Pensaernïol Siartredig, Swyddogion Cynllunio, Syrfewyr ac Adeiladwyr Proffesiynol",
        "en": "Architects, Chartered Architectural Technologists, Planning Officers, Surveyors and Construction Professionals"
    },
    "architects_town_planners_and_surveyors": {
        "cy": "Penseiri, cynllunwyr tref, syrfewyr",
        "en": "Architects, town planners, surveyors"
    },
    "artistic_and_literary_occupations": {
        "cy": "Galwedigaethau artistig a llenyddol",
        "en": "Artistic and literary occupations"
    },
    "artistic_literary_and_media_occupations": {
        "cy": "Galwedigaethau Artistig, Llenyddol a'r Cyfryngau",
        "en": "Artistic, literary and media occupations"
    },
    "business_and_finance_associate_professionals": {
        "cy": "Gweithwyr proffesiynol ym maes busnes a chyllid cysylltiol",
        "en": "Business and finance associate professionals"
    },
    "business_and_financial_project_management_professionals": {
        "cy": "Gweithwyr Proffesiynol ym maes Rheoli Prosiectau Busnes ac Ariannol",
        "en": "Business and Financial Project Management Professionals"
    },
    "business_and_public_service_associate_professionals": {
        "cy": "Gweithwyr Cyswllt Proffesiynol ym maes Busnes a Gwasanaeth Cyhoeddus",
        "en": "Business and public service associate professionals"
    },
    "business_and_statistical_professionals": {
        "cy": "Gweithwyr proffesiynol busnes ac ystadegol",
        "en": "Business and statistical professionals"
    },
    "business_research_and_administrative_professionals": {
        "cy": "Gweithwyr Proffesiynol ym maes Busnes, Ymchwil a Gweinyddiaeth",
        "en": "Business, Research and Administrative Professionals"
    },
    "caring_personal_service_occupations": {
        "cy": "Galwedigaethau gofal a gwasanaeth personol",
        "en": "Caring personal service occupations"
    },
    "caring_personal_services": {
        "cy": "Gwasanaethau Gofalu Personol",
        "en": "Caring personal services"
    },
    "childcare_and_related_personal_services": {
        "cy": "Gwasanaethau Personol Gofal Plant a Gwasanaethau Cysylltiedig",
        "en": "Childcare and related personal services"
    },
    "community_and_civil_enforcement_occupations": {
        "cy": "Galwedigaethau Gorfodi Sifil a Chymunedol",
        "en": "Community and Civil Enforcement Occupations"
    },
    "conservation_and_environment_professionals": {
        "cy": "Gweithwyr Proffesiynol Cadwraeth a'r Amgylchedd",
        "en": "Conservation and environment professionals"
    },
    "conservation_associate_professionals": {
        "cy": "Gweithwyr proffesiynol ym maes cadwraeth",
        "en": "Conservation associate professionals"
    },
    "corporate_managers_and_senior_officials": {
        "cy": "Rheolwyr corfforaethol ac uwch swyddogion",
        "en": "Corporate managers and senior officials"
    },
    "customer_service_occupations": {
        "cy": "Galwedigaethau Gwasanaeth cwsmeriaid",
        "en": "Customer service occupations"
    },
    "design_associate_professionals": {
        "cy": "Gweithwyr proffesiynol ym maes Dylunio",
        "en": "Design associate professionals"
    },
    "design_occupations": {
        "cy": "Galwedigaethau Dylunio",
        "en": "Design occupations"
    },
    "draughtspersons_and_building_inspectors": {
        "cy": "Drafftsmyn ac arolygwyr adeiladu",
        "en": "Draughtspersons and building inspectors"
    },
    "elementary_occupations": {
        "cy": "Galwedigaethau elfennol",
        "en": "Elementary occupations"
    },
    "engineering_professionals": {
        "cy": "Gweithwyr Proffesiynol Peirianneg",
        "en": "Engineering professionals"
    },
    "finance_professionals": {
        "cy": "Gweithwyr Cyllid Proffesiynol ",
        "en": "Finance Professionals"
    },
    "financial_institution_and_office_managers": {
        "cy": "Rheolwyr sefydliad ariannol a swyddfa",
        "en": "Financial institution and office managers"
    },
    "functional_managers": {
        "cy": "Rheolwyr gweithredol",
        "en": "Functional managers"
    },
    "health_associate_professionals": {
        "cy": "Gweithwyr Proffesiynol Cyswllt ym maes Iechyd",
        "en": "Health associate professionals"
    },
    "health_professionals": {
        "cy": "Gweithwyr iechyd proffesiynol",
        "en": "Health professionals"
    },
    "information_and_communication_technology_professionals": {
        "cy": "Gweithwyr proffesiynol ym maes technoleg gwybodaeth a chyfathrebu",
        "en": "Information and communication technology professionals"
    },
    "information_technology_and_telecommunications_professionals": {
        "cy": "Gweithwyr Proffesiynol Technoleg Gwybodaeth a Thelathrebu",
        "en": "Information technology and telecommunications professionals"
    },
    "information_technology_professionals": {
        "cy": "Gweithwyr Proffesiynol Technoleg Gwybodaeth",
        "en": "Information Technology Professionals"
    },
    "it_service_delivery_occupations": {
        "cy": "Galwedigaethau darparu gwasanaethau TG",
        "en": "IT service delivery occupations"
    },
    "legal_associate_professionals": {
        "cy": "Gweithwyr proffesiynol cysylltiol Cyfreithiol",
        "en": "Legal associate professionals"
    },
    "legal_professionals": {
        "cy": "Gweithwyr Cyfreithiol Proffesiynol",
        "en": "Legal professionals"
    },
    "leisure_and_other_personal_service_occupations": {
        "cy": "Galwedigaethau hamdden a gwasanaethau personol eraill",
        "en": "Leisure and other personal service occupations"
    },
    "leisure_travel_and_related_personal_service_occupations": {
        "cy": "Hamdden, teithio a galwedigaethau gwasanaeth personol cysylltiedig",
        "en": "Leisure, travel and related personal service occupations"
    },
    "librarians_and_related_professionals": {
        "cy": "Llyfrgellwyr a Gweithwyr Proffesiynol Cysylltiedig",
        "en": "Librarians and Related Professionals"
    },
    "managers_directors_and_senior_officials": {
        "cy": "Rheolwyr, Cyfarwyddwyr ac Uwch Swyddogion",
        "en": "Managers, directors and senior officials"
    },
    "managers_in_distribution_storage_and_retailing": {
        "cy": "Rheolwyr mewn dosbarthu, storio a manwerthu",
        "en": "Managers in distribution, storage and retailing"
    },
    "media_associate_professionals": {
        "cy": "Gweithwyr proffesiynol ym maes Cyfryngau",
        "en": "Media associate professionals"
    },
    "media_professionals": {
        "cy": "Gweithwyr Proffesiynol y Cyfryngau",
        "en": "Media Professionals"
    },
    "medical_practitioners": {
        "cy": "Ymarferwyr Meddygol",
        "en": "Medical Practitioners"
    },
    "natural_and_social_science_professionals": {
        "cy": "Gweithwyr Proffesiynol Gwyddor naturiol a Chymdeithasol",
        "en": "Natural and social science professionals"
    },
    "nursing_and_midwifery_professionals": {
        "cy": "Gweithwyr Proffesiynol Nyrsio a Bydwreigiaeth",
        "en": "Nursing and midwifery professionals"
    },
    "nursing_professionals": {
        "cy": "Gweithwyr Nyrsio Proffesiynol",
        "en": "Nursing Professionals"
    },
    "other_educational_professionals": {
        "cy": "Gweithwyr Addysg Proffesiynol Eraill",
        "en": "Other Educational Professionals"
    },
    "other_health_professionals": {
        "cy": "Gweithwyr Iechyd Proffesiynol Eraill",
        "en": "Other Health Professionals"
    },
    "process_plant_and_machine_operatives": {
        "cy": "Gweithwyr prosesau, offer a pheiriannau",
        "en": "Process, plant and machine operatives"
    },
    "production_managers": {
        "cy": "Rheolwyr cynhyrchu",
        "en": "Production managers"
    },
    "protective_service_occupations": {
        "cy": "Galwedigaethau gwasanaeth amddiffynnol",
        "en": "Protective service occupations"
    },
    "protective_service_officers": {
        "cy": "Swyddogion y gwasanaeth amddiffynnol",
        "en": "Protective service officers"
    },
    "public_service_and_other_associate_professionals": {
        "cy": "Gwasanaethau cyhoeddus a gweithwyr proffesiynol cysylltiol eraill",
        "en": "Public service and other associate professionals"
    },
    "public_service_professionals": {
        "cy": "Gweithwyr proffesiynol ym maes gwasanaeth cyhoeddus",
        "en": "Public service professionals"
    },
    "quality_and_customer_care_managers": {
        "cy": "Rheolwyr ansawdd a gofal cwsmeriaid",
        "en": "Quality and customer care managers"
    },
    "quality_and_regulatory_professionals": {
        "cy": "Gweithwyr Proffesiynol Ansawdd a Rheoleiddio",
        "en": "Quality and Regulatory Professionals"
    },
    "research_and_development_managers": {
        "cy": "Rheolwyr Ymchwil a Datblygu",
        "en": "Research and development managers"
    },
    "research_and_development_randd_and_other_research_professionals": {
        "cy": "Ymchwil a Datblygu (YaD) a Gweithwyr Proffesiynol Ymchwil Eraill",
        "en": "Research and Development (RandD) and Other Research Professionals"
    },
    "research_professionals": {
        "cy": "Gweithwyr proffesiynol ym maes Ymchwil",
        "en": "Research professionals"
    },
    "sales_and_related_associate_professionals": {
        "cy": "Gweithwyr proffesiynol syn gysylltiedig â Gwerthu",
        "en": "Sales and related associate professionals"
    },
    "sales_assistants_and_retail_cashiers": {
        "cy": "Cynorthwywyr gwerthu ac arianwyr manwerthu",
        "en": "Sales assistants and retail cashiers"
    },
    "sales_occupations": {
        "cy": "Galwedigaethau Gwerthu",
        "en": "Sales occupations"
    },
    "sales_related_occupations": {
        "cy": "Galwedigaethau Gwerthu cysylltiedig",
        "en": "Sales related occupations"
    },
    "science_and_engineering_technicians": {
        "cy": "Technegwyr gwyddoniaeth a pheirianneg",
        "en": "Science and engineering technicians"
    },
    "science_engineering_and_technology_associate_professionals": {
        "cy": "Gweithwyr Proffesiynol Cysylltiol Gwyddoniaeth, Peirianneg a Thechnoleg ",
        "en": "Science, engineering and technology associate professionals"
    },
    "science_professionals": {
        "cy": "Gweithwyr proffesiynol gwyddoniaeth",
        "en": "Science professionals"
    },
    "secretarial_and_related_occupations": {
        "cy": "Galwedigaethau ysgrifenyddol a chysylltiedig",
        "en": "Secretarial and related occupations"
    },
    "skilled_trades_occupations": {
        "cy": "Galwedigaethau crefftau medrus",
        "en": "Skilled trades occupations"
    },
    "social_welfare_associate_professionals": {
        "cy": "Gweithwyr proffesiynol ym maes lles cymdeithasol",
        "en": "Social welfare associate professionals"
    },
    "sports_and_fitness_occupations": {
        "cy": "Galwedigaethau Chwaraeon a Ffitrwydd",
        "en": "Sports and fitness occupations"
    },
    "teaching_and_childcare_associate_professionals": {
        "cy": "Gweithwyr Proffesiynol Cyswllt ym maes Addysgu a Gofal Plant",
        "en": "Teaching and Childcare Associate Professionals"
    },
    "teaching_and_childcare_support_occupation": {
        "cy": "Galwedigaethau Cymorth Addysgu a Gofal Plant",
        "en": "Teaching and Childcare Support Occupation"
    },
    "teaching_and_educational_professionals": {
        "cy": "Gweithwyr Proffesiynol Addysgu ac Addysgol ",
        "en": "Teaching and educational professionals"
    },
    "teaching_professionals": {
        "cy": "Gweithwyr Addysgu Proffesiynol",
        "en": "Teaching Professionals"
    },
    "therapists": {
        "cy": "Therapyddion",
        "en": "Therapists"
    },
    "therapy_professionals": {
        "cy": "Gweithwyr Therapi Proffesiynol",
        "en": "Therapy professionals"
    },
    "transport_associate_professionals": {
        "cy": "Gweithwyr proffesiynol  ym maes Cludiant",
        "en": "Transport associate professionals"
    },
    "veterinarians": {
        "cy": "Milfeddygon",
        "en": "Veterinarians"
    },
    "veterinary_nurses": {
        "cy": "Nyrsys Milfeddygol",
        "en": "Veterinary nurses"
    },
    "web_and_multimedia_design_professionals": {
        "cy": "Gweithwyr Proffesiynol Dylunio'r We ac Amlgyfrwng",
        "en": "Web and Multimedia Design Professionals"
    },
    "welfare_and_housing_associate_professionals": {
        "cy": "Gweithwyr Proffesiynol Cyswllt ym maes Lles a Thai",
        "en": "Welfare and housing associate professionals"
    },
    "welfare_professionals": {
        "cy": "Gweithwyr Proffesiynol Llesiant",
        "en": "Welfare Professionals"
    }
}

OPTIONALS = {
    'not_available': {
        'en': 'Not Available',
        'cy': 'Ddim ar gael'
    },
    'optional': {
        "en": 'Optional',
        'cy': 'Dewisol'
    },
    'compulsory': {
        "en": 'Compulsory',
        'cy': 'Gorfodol'
    },
    'yes': {
        'en': 'Yes',
        'cy': 'Ydy'
    },
}

DICT = {
    "a_level_similar": {
        "cy": "Safonau Uwch, Cymwysterau Advanced Higher neu debyg",
        "en": "A-levels, Advanced Highers or similar"
    },
    "about": {
        "cy": "Ynghylch",
        "en": "About"
    },
    # TODO: "about our data link" can be removed once the wagtail panels have been
    # changed to only contain the source link
    "about_our_data_link": {
        "cy": "https://discoveruni.gov.uk/cy/yngl%C5%B7n-%C3%A2n-data-about-our-data-cy/#arolwg_cenedlaethol_o_fyfyrwyr",
        "en": "https://www.discoveruni.gov.uk/about-our-data/#the_national_student_survey"
    },
    "access_course": {
        "cy": "Wedi cwblhau cwrs mynediad",
        "en": "Completed Access course"
    },
    "accommodation": {
        "cy": "Costau a gwybodaeth am lety",
        "en": "Accommodation costs and information"
    },
    "accreditation_description": {
        "cy": "Cwrs wedi'i achredu'n broffesiynol yw cwrs sydd wedi'i gymeradwyo neu ei ategu gan un neu fwy o gyrff proffesiynol. Mae hyn oherwydd bod dysg a chyflawniad graddedigion yn bodloni'r meincnodau a'r safonau proffesiynol a osodir gan y corff achredu.",
        "en": "A professionally accredited course is one which has been approved or endorsed by one or more professional bodies. This is because the learning and achievement of graduates meets the professional benchmarks and standards set by the accrediting body."
    },
    "accreditation_link_label": {
        "cy": "Darllen mwy am achrediad proffesiynol",
        "en": "Read more about professional accreditation"
    },
    "accreditation_link_url": {
        "cy": "https://discoveruni.gov.uk/cy/how-choose-course-cy/rhagolygon-cyflogaeth-employment-prospects/#achrediad_proffesiynol",
        "en": "https://discoveruni.gov.uk/how-do-i-choose-course/employment-prospects/#professional_accreditation"
    },
    "accreditation_need_to_know": {
        "cy": "Yr hyn y mae angen i chi ei wybod am achrediad proffesiynol",
        "en": "What you need to know about professional accreditation"
    },
    "across_uk": {
        "cy": "ar draws y DU",
        "en": "across the UK"
    },
    "add_saved_course": {
        "cy": "Ychwanegu cwrs wedi’i gadw",
        "en": "Add saved course"
    },
    "add_two_courses": {
        "cy": "Ychwanegwch 2 gwrs i ddefnyddio’r offeryn cymharu",
        "en": "Add 2 courses to use the comparison tool"
    },
    "address": {
        "cy": "Cyfeiriad",
        "en": "Address"
    },
    "after_1_year_overview_2": {
        "cy": "myfyrwyr",
        "en": "students"
    },
    "after_1_year_overview_3": {
        "cy": "or rhai y gofynnwyd iddynt",
        "en": "of those who were asked"
    },
    "after_course_graph_desc": {
        "cy": " o fyfyrwyr ar ôl y cwrs sydd yn",
        "en": " of students after the course who are"
    },
    "after_course_graph_title": {
        "cy": "Graff yn dangos nifer y myfyrwyr ar ôl y cwrs sydd",
        "en": "Graph showing number of students after the course who are"
    },
    "after_one_year_graph_desc": {
        "cy": " o fyfyrwyr flwyddyn ar ôl y cwrs sydd",
        "en": " of students one year after the course who"
    },
    "after_one_year_graph_title": {
        "cy": "Graff yn dangos nifer y myfyrwyr sydd, flwyddyn ar ôl y cwrs, yn",
        "en": "Graph showing number of students one year after the course who"
    },
    "answer_4_questions": {
        "cy": "Atebwch 4 cwestiwn er mwyn darganfod cyrsiau sy'n berthnasol i mi",
        "en": "Answer 4 questions to find courses relevant to me"
    },
    "any_changes_in_the_course_or_teaching_have_been_communicated_effectively": {
        "cy": "Cafwyd cyfathrebu effeithiol ynghylch unrhyw newidiadau o ran y cwrs neu'r addysgu",
        "en": "Any changes in the course or teaching have been communicated effectively"
    },
    "apply_filters": {
        "cy": "Gweithredu hidlyddion",
        "en": "Apply filters"
    },
    "assessment_method": {
        "cy": "Dull asesu'r cwrs",
        "en": "How the course is assessed"
    },
    "at": {
        "cy": "yn:",
        "en": "at:"
    },
    "average_earnings_course_overview_1": {
        "cy": "Enillion cyfartalog",
        "en": "Average Earnings"
    },
    "average_earnings_course_overview_2a": {
        "cy": "15 mis ar ôl y cwrs",
        "en": "15 months after the course"
    },
    "average_earnings_course_overview_2b": {
        "cy": "3 blynedd ar ôl y cwrs",
        "en": "3 years after the course"
    },
    "average_earnings_course_overview_3": {
        "cy": "Ewch i’r adran Enillion",
        "en": "Go to Earnings"
    },
    "average_earnings_year_range": {
        "cy": "fyfyrwyr a raddiodd yn ystod",
        "en": "students graduating during"
    },
    "baccalaureate": {
        "cy": "Bagloriaeth",
        "en": "Baccalaureate"
    },
    "back": {
        "cy": "Yn ôl",
        "en": "Back"
    },
    "back_to_results": {
        "cy": "Canlyniadau",
        "en": "Back"
    },
    "begin": {
        "cy": "Dechrau",
        "en": "Begin"
    },
    "bookmark_course": {
        "cy": "Nodi cwrs",
        "en": "Bookmark course"
    },
    "bookmark_courses_link": {
        "cy": "./cy/rheoli-nodau-tudalen/",
        "en": "./bookmarks-manage/"
    },
    "bookmarked_courses": {
        "cy": "cyrsiau a nodwyd",
        "en": "bookmarked courses"
    },
    "break_from_studies": {
        "cy": "Yn cymryd egwyl o astudio",
        "en": "Are taking a break from their studies"
    },
    "bronze": {
        "cy": "Efydd",
        "en": "Bronze"
    },
    "by_course_location": {
        "cy": "Chwilio yn ôl cwrs neu leoliad",
        "en": "Search by course or location"
    },
    "can_compare_courses": {
        "cy": "Gymharu cyrsiau",
        "en": "Compare courses"
    },
    "chart_label_explained": {
        "cy": "Esboniad ynghylch labeli'r siart",
        "en": "Chart labels explained"
    },
    "clear_all": {
        "cy": "Clirio popeth",
        "en": "Clear all"
    },
    "clear_filters": {
        "cy": "Clirio'r Hidlau",
        "en": "Clear Filters"
    },
    "close": {
        "cy": "Cau",
        "en": "Close"
    },
    "compare": {
        "cy": "Cymharu",
        "en": "Compare"
    },
    "compare_7_courses": {
        "cy": "Cymharwch hyd at 7 o gyrsiau",
        "en": "Compare up to 7 courses"
    },
    "compare_course": {
        "cy": "Cymharu'r cwrs",
        "en": "Compare course"
    },
    "compare_courses": {
        "cy": "Cymharu cyrsiau",
        "en": "Compare courses"
    },
    "completed_course": {
        "cy": "Wedi cwblhau'r cwrs",
        "en": "Have completed their studies"
    },
    "compulsory": {
        "cy": "Gorfodol",
        "en": "Compulsory"
    },
    "cookie_message": {
        "cy": "Mae’r wefan hon yn defnyddio cwcis i storio gwybodaeth ar eich cyfrifiadur.",
        "en": "This website uses cookies to store information on your computer."
    },
    "cookie_more": {
        "cy": "Hoffwn wybod mwy",
        "en": "I’d like to find out more"
    },
    "cookie_ok": {
        "cy": "Rwy’n fodlon â’r cwcis",
        "en": "I’m happy with cookies"
    },
    "copyright": {
        "cy": "Hawlfraint 2020. Cedwir Pob Hawl",
        "en": "2020 Copyright. All rights reserved."
    },
    "costs_and_support": {
        "cy": "Costau a chymorth",
        "en": "Costs and support"
    },
    "countries": {
        "cy": "Gwledydd",
        "en": "Countries"
    },
    "course": {
        "cy": "cyrsiau",
        "en": "courses"
    },
    "course_added": {
        "cy": "cwrs wedi’i ychwanegu at y ",
        "en": "course added to "
    },
    "course_comparison_link": {
        "cy": "./cy/cymharu-cyrsiau/",
        "en": "./course-comparison/"
    },
    "course_cost": {
        "cy": "Costau'r cwrs",
        "en": "Course costs"
    },
    "course_details": {
        "cy": "Manylion y cwrs",
        "en": "Course details"
    },
    "course_details_joint_overview_1": {
        "cy": "Beth y mae angen i chi ei wybod am y cwrs yma",
        "en": "What you need to know about this course"
    },
    "course_details_joint_overview_2": {
        "cy": "Mae’r cwrs yma’n cynnwys gwybodaeth a data ar gyfer mwy nag un pwnc. Pwrpas y llabedau isod yw eich helpu i weld pa bwnc y mae’r data yn berthnasol iddo",
        "en": "This course has information and data for more than one subject. The tabs below are there to help you see which subject the data relates to."
    },
    "course_details_joint_overview_3": {
        "cy": "Darllen mwy am gyrsiau sy’n cynnwys amryw o bynciau",
        "en": "Read more about courses with multiple subjects"
    },
    "course_details_joint_overview_4": {
        "cy": "https://discoveruni.gov.uk/cy/yngl%C5%B7n-%C3%A2n-data-about-our-data-cy/#data_a_gasglwyd_gan_brifysgolion_a_cholegau_ar_fyfyrwyr_unigol",
        "en": "https://discoveruni.gov.uk/about-our-data/#understanding_the_data"
    },
    "course_finder": {
        "cy": "Cael Hyd i Gwrs",
        "en": "Course Finder"
    },
    "course_length_not_available": {
        "cy": "Nid yw hyd y cwrs ar gael",
        "en": "Length of course is not available"
    },
    "course_level_msg": {
        "cy": "Sylwch: nid yw'r wybodaeth ganlynol yn cynnwys unrhyw ddata ar gyfer graddau cyntaf (fel BA, BSc neu Gwrs Meistr Integredig). Yn lle hynny, mae'n dangos gwybodaeth ar gyfer cymwysterau israddedig eraill - mae hyn yn cynnwys Tystysgrif Addysg Uwch, Diploma Addysg Uwch a Gradd Sylfaen ymhlith eraill",
        "en": "Please note: the following information does not contain any data for first degrees (such as BA, BSc, or Integrated Masters). Instead it is displaying information for other undergraduate qualifications – this includes CertHE, DipHE and FD among others"
    },
    "course_name": {
        "cy": "Enw'r cwrs",
        "en": "Course name"
    },
    "course_name_search_box": {
        "cy": "Blwch chwilio enw’r cwrs",
        "en": "Course name search box"
    },
    "course_page": {
        "cy": "Tudalen y cwrs",
        "en": "Course page"
    },
    "course_removed": {
        "cy": "Cwrs wedi’i ddileu o'r ",
        "en": "Course removed from "
    },
    "course_search": {
        "cy": "Chwilio am Gwrs ",
        "en": "Course search"
    },
    "course_search_form_inputs": {
        "cy": "Mewnbynnau ffurflen chwilio am gwrs",
        "en": "Course search form inputs"
    },
    "course_too_many": {
        "cy": "yw'r nifer uchaf o nodau tudalen y gallwch eu hychwanegu",
        "en": "is the maximum number of bookmarks."
    },
    "course_wizard": {
        "cy": "Dewin Cwrs",
        "en": "Course Wizard"
    },
    "course_wizard_start_now": {
        "cy": "Dechrau Nawr",
        "en": "Start Now"
    },
    "course_wizard_start_now_url": {
        "cy": "/cy/search-landing-cy/course-finder-choose-country-cy/",
        "en": "/search-landing-page/course-finder-choose-country/"
    },
    "courses": {
        "cy": "cwrs/cyrsiau",
        "en": "course(s)"
    },
    "courses_added": {
        "cy": "cyrsiau wedi’u hychwanegu at y ",
        "en": "courses added to "
    },
    "courses_selected": {
        "cy": "cwrs wedi’u dewis",
        "en": "course(s) selected"
    },
    "courses_to_view": {
        "cy": "i weld cyrsiau a gadwyd ochr wrth ochr",
        "en": "to view saved courses side-by-side"
    },
    "covid_19_info": {
        "cy": "Gwybodaeth diweddaraf Coronafeirws (COVID-19)",
        "en": "Coronavirus (COVID-19) latest information"
    },
    "data_for": {
        "cy": "Data ar gyfer",
        "en": "Data for"
    },
    "data_from": {
        "cy": "Data gan",
        "en": "Data from"
    },
    "data_from_html": {
        "cy": "<div class=\"d-inline d-md-none\"><i class=\"fas fa-user-alt \"></i></div><div id=\"sample-size-text\" class=\"d-none d-md-inline text-left\">Data gan</div>",
        "en": "<div class=\"d-inline d-md-none\" ><i class=\"fas fa-user-alt \"></i></div><div id=\"sample-size-text\" class=\"d-none d-md-inline text-left\">Data from</div>"
    },
    "data_from_html_average_earnings_year_range": {
        "cy": "<div class=\"d-inline d-md-none\"><i class=\"fas fa-user-alt \"></i></div><div id=\"sample-size-text\" class=\"d-none d-md-inline\">Data o</div>",
        "en": "<div class=\"d-inline d-md-none\" ><i class=\"fas fa-user-alt \"></i></div><div id=\"sample-size-text\" class=\"d-none d-md-inline\">Data from</div>"
    },
    "data_ind_stud_coll_dir": {
        "cy": "Data ar gyfer myfyrwyr unigol a gasglwyd yn uniongyrchol o brifysgolion a cholegau",
        "en": "Data for individual students collected directly from universities and colleges"
    },
    "default_region": {
        "cy": "y DU",
        "en": "the UK"
    },
    "degree": {
        "cy": "Gradd",
        "en": "Degree"
    },
    "did_not_participate": {
        "cy": "Heb gymryd rhan",
        "en": "Did not participate"
    },
    "disclaimer": {
        "cy": "Mae enwau'r Prifysgolion fel y'u darperir gan Gofrestr y DU o Ddarparwyr Dysgu. Os nad yw'r enw Cymraeg yn bresennol, chwiliwch amdano gan ddefnyddio'i enw Saesneg.",
        "en": ""
    },
    "distance": {
        "cy": "Pellter",
        "en": "Distance"
    },
    "distance_learning": {
        "cy": "Dysgu o bell",
        "en": "Distance learning"
    },
    "distance_learning_values": {
        "0": {
            "cy": "Ddim ar gael",
            "en": "Not Available"
        },
        "1": {
            "cy": "Ydy",
            "en": "Yes"
        },
        "2": {
            "cy": "Dewisol",
            "en": "Optional"
        },
        "Course is available other than by distance learning": {
            "cy": "Ddim ar gael",
            "en": "Not Available"
        }
    },
    "doing_further_study": {
        "cy": "Yn astudio ymhellach",
        "en": "Doing further study"
    },
    "dont_mind": {
        "cy": "Does dim ots gen i",
        "en": "I don't mind"
    },
    "dont_narrow": {
        "cy": "peidio cyfyngu'r chwiliad",
        "en": "don't narrow search"
    },
    "employment_course_overview_1": {
        "cy": "Cyflogaeth",
        "en": "Employment"
    },
    "employment_course_overview_2": {
        "cy": "yn symud ymlaen i weithio ac/neu astudio o fewn 15 mis ar ôl y cwrs",
        "en": "go on to work and / or study within 15 months after the course"
    },
    "employment_course_overview_3": {
        "cy": "Ewch i’r adran Cyflogaeth",
        "en": "Go to Employment"
    },
    "employment_details": {
        "cy": "Gwybodaeth am gyflogaeth",
        "en": "Employment information"
    },
    "employment_type_unknown": {
        "cy": "Gyflogir ar ôl gorffen y cwrs ond nad ydym yn gwybod pa fath o swydd sydd ganddynt",
        "en": "Employed after finishing the course but employment type is not known"
    },
    "england": {
        "cy": "Lloegr",
        "en": "England"
    },
    "enhanced_degree": {
        "cy": "",
        "en": "Enhanced first degree (e.g. MEng)"
    },
    "enter_3_characters": {
        "cy": "Rhowch 3 nod o leiaf er mwyn chwilio",
        "en": "Please enter at least 3 characters to search"
    },
    "enter_postcode": {
        "cy": "Nodwch y cod post",
        "en": "Enter postcode"
    },
    "entrance_data_need_to_know": {
        "cy": "Yr hyn y mae angen ichi wybod am ddata mynediad",
        "en": "What you need to know about entry data"
    },
    "entrance_data_quals_students_had": {
        "cy": "Dyma'r cymwysterau a oedd gan fyfyrwyr wrth gael eu derbyn ar y cwrs yma. Nid rhestr o gymwysterau sydd eu hangen ar rywun er mwyn cael eu derbyn ar y cwrs yw hon",
        "en": "These are the qualifications students had when they were accepted onto this course. This is not a list of qualifications a person needs to have to be accepted onto this course"
    },
    "entrance_data_read_more": {
        "cy": "Darllen mwy am ddata mynediad",
        "en": "Read more about entry data"
    },
    "entrance_data_read_more_url": {
        "cy": "https://discoveruni.gov.uk/cy/yngl%C5%B7n-%C3%A2n-data-about-our-data-cy/#data_a_gasglwyd_gan_brifysgolion_a_cholegau_ar_fyfyrwyr_unigol",
        "en": "https://discoveruni.gov.uk/about-our-data/#data_collected_from_universities_and_colleges_on_individual_students"
    },
    "entry_graph_desc": {
        "cy": " Nifer y myfyrwyr a ddechreuodd y cwrs gyda",
        "en": " of students entered the course with"
    },
    "entry_graph_title": {
        "cy": "Graff yn dangos nifer y myfyrwyr sy’n dechrau’r cwrs gyda ",
        "en": "Graph showing number of students entering the course with"
    },
    "entry_overview_2": {
        "cy": "myfyrwyr",
        "en": "students"
    },
    "entry_overview_3": {
        "cy": "or rhai y gofynnwyd iddynt",
        "en": "of those who were asked"
    },
    "facebook_link": {
        "cy": "Dolen Facebook",
        "en": "Facebook link"
    },
    "feedback_button": {
        "cy": "adborth",
        "en": "feedback"
    },
    "feedback_error": {
        "cy": "Mae'n ddrwg gennym, aeth rhywbeth o'i le wrth ichi roi adborth. Rhowch gynnig arall ymhen ychydig.",
        "en": "Sorry something went wrong submitting your feedback, please try again later."
    },
    "feedback_form": {
        "cy": "Fersiwn beta yw’r wefan hon. Rydym yn croesawu eich ",
        "en": "This site is in beta. We welcome your "
    },
    "feedback_on_my_work_has_been_timely": {
        "cy": "Mae’r adborth ar fy ngwaith i wedi bod yn amserol",
        "en": "Feedback on my work has been timely"
    },
    "feedback_thanks": {
        "cy": "Diolch am eich adborth",
        "en": "Thanks for your feedback."
    },
    "filter": {
        "cy": "Hidlo",
        "en": "Filter"
    },
    "filter_by": {
        "cy": "Hidlo gan",
        "en": "Filter by"
    },
    "filter_not_applicable": {
        "cy": "Nid yw'r hidlydd hwn yn berthnasol i gyrsiau dysgu o bell.",
        "en": "This filter is not applicable for distance learning courses."
    },
    "filter_sort_by_subject_add_more_filters": {
        "cy": "Defnyddiwch fwy o hidlwyr i'w didoli yn ôl pwnc",
        "en": "Please apply more filters to sort by subject"
    },
    "filters": {
        "cy": "Hidlau",
        "en": "Filters"
    },
    "financial_support_details": {
        "cy": "Cymorth ariannol",
        "en": "Financial support"
    },
    "find_out_more": {
        "cy": "Mwy o wybodaeth",
        "en": "Find out more"
    },
    "first_degree": {
        "cy": "Gradd Cyntaf (BA, BSc, Gradd Meistr Integredig)",
        "en": "First degree (e.g. BA, BSc, Integrated Masters)"
    },
    "foundation_course": {
        "cy": "Cwrs sylfaen",
        "en": "Foundation course"
    },
    "foundation_degree": {
        "cy": "",
        "en": "Foundation degree (e.g. FD, FDEd)"
    },
    "foundation_year": {
        "cy": "Blwyddyn sylfaen",
        "en": "Foundation year"
    },
    "full_time": {
        "cy": "Llawn-amser",
        "en": "Full time"
    },
    "gold": {
        "cy": "Aur",
        "en": "Gold"
    },
    "good_advice_was_available_when_i_needed_to_make_study_choices_on_my_course": {
        "cy": "Roedd cyngor da ar gael i mi pan oeddwn i eisiau gwneud dewisiadau astudio ar fy nghwrs",
        "en": "Good advice was available when I needed to make study choices on my course"
    },
    "guidance_comparing": {
        "cy": "Canllawiau ar gymharu cyrsiau",
        "en": "Guidance on comparing courses"
    },
    "guidance_text": {
        "cy": "Mae'r data hyn ar gyrsiau'n rhoi cipolwg o brofiadau ar adeg benodol. Gallai eich profiad chi fod yn wahanol.  Daw rhywfaint o'r data gan fyfyrwyr a gymerodd ran yn yr arolwg yn ystod y pandemig. <a href='https://www.discoveruni.gov.uk/cy/yngl%C5%B7n-%C3%A2n-data-about-our-data-cy/' target='_blank' class='blue-text'>Mae rhagor o wybodaeth</a> ar gael ynghylch sut i ddefnyddio'r data hyn wrth benderfynu beth i'w astudio ac ymhle.",
        "en": "This course data presents a snapshot at a point in time, your experience may be different. Some data is from students surveyed during the pandemic. <a href='https://www.discoveruni.gov.uk/about-our-data/' target='_blank' class='blue-text'>Find out more</a> about how to use this data when making decisions about where and what to study."
    },
    "guidance_title": {
        "cy": "Beth y mae angen ichi ei ystyried wrth gymharu cyrsiau",
        "en": "What you need to consider when comparing courses"
    },
    "health_and_social_services_managers": {
        "cy": "Rheolwyr Iechyd a gwasanaethau cymdeithasol",
        "en": "Health and social services managers"
    },
    "highly_skilled": {
        "cy": "Mewn swydd lle mae angen lefel uchel o sgiliau",
        "en": "In highly skilled work"
    },
    "hnc": {
        "cy": "",
        "en": "Higher National Certificate (HNC)"
    },
    "hnd": {
        "cy": "",
        "en": "Higher National Diploma (HND)"
    },
    "home_page_video": {
        "cy": "Fideo hafan",
        "en": "Home page video"
    },
    "home_page_video_link": {
        "cy": "https://www.youtube.com/embed/ZMJqdQhtO3E",
        "en": "https://www.youtube.com/embed/W7jJ03_UjUg"
    },
    "how_improve": {
        "cy": "Dywedwch wrthym am eich profiad",
        "en": "Please tell us about your experience"
    },
    "how_to_search_for_course": {
        "cy": "Sut i chwilio am gyrsiau",
        "en": "How to search for courses"
    },
    "how_useful": {
        "cy": "A oedd y dudalen hon yn ddefnyddiol i chi?",
        "en": "How was this page useful to you?"
    },
    "i_feel_part_of_a_community_of_staff_and_students": {
        "cy": "Rydw i’n teimlo’n rhan o gymuned o staff a myfyrwyr",
        "en": "I feel part of a community of staff and students"
    },
    "i_have_been_able_to_access_course_specific_resources_eg_equipment_facilities_software_collections_when_i_needed_to": {
        "cy": "Rydw i wedi gallu cael mynediad at adnoddau penodol i gwrs (e.e. offer, cyfleusterau, meddalwedd, casgliadau) pan oedd angen i mi wneud hynny",
        "en": "I have been able to access course-specific resources (e.g. equipment, facilities, software, collections) when I needed to"
    },
    "i_have_been_able_to_contact_staff_when_i_needed_to": {
        "cy": "Rydw i wedi gallu cysylltu â staff pan oeddwn i angen gwneud hynny",
        "en": "I have been able to contact staff when I needed to"
    },
    "i_have_had_the_right_opportunities_to_provide_feedback_on_my_course": {
        "cy": "Rydw i wedi cael cyfleoedd priodol i roi adborth ar fy nghwrs",
        "en": "I have had the right opportunities to provide feedback on my course"
    },
    "i_have_had_the_right_opportunities_to_work_with_other_students_as_part_of_my_course": {
        "cy": "Rydw i wedi cael cyfleoedd priodol i weithio gyda myfyrwyr eraill fel rhan o'm cwrs",
        "en": "I have had the right opportunities to work with other students as part of my course"
    },
    "i_have_received_helpful_comments_on_my_work": {
        "cy": "Rydw i wedi cael sylwadau defnyddiol ar fy ngwaith",
        "en": "I have received helpful comments on my work"
    },
    "i_have_received_sufficient_advice_and_guidance_in_relation_to_my_course": {
        "cy": "Rydw i wedi cael digon o gyngor ac arweiniad mewn perthynas â'm cwrs",
        "en": "I have received sufficient advice and guidance in relation to my course"
    },
    "i_received_appropriate_supervision_on_placements": {
        "cy": "Fe dderbyniais oruchwyliaeth briodol yn ystod fy lleoliad gwaith",
        "en": "I received appropriate supervision on placement(s)"
    },
    "i_received_sufficient_preparatory_information_prior_to_my_placements": {
        "cy": "Fe dderbyniais wybodaeth ddigonol i fy mharatoi ar gyfer lleoliad(au) gwaith",
        "en": "I received sufficient preparatory information prior to my placement(s)"
    },
    "i_was_allocated_placements_suitable_for_my_course": {
        "cy": "Pennwyd lleoliad(au) gwaith addas ar gyfer fy nghwrs",
        "en": "I was allocated placement(s) suitable for my course"
    },
    "i_was_given_opportunities_to_meet_my_required_practice_learning_outcomescompetences": {
        "cy": "Cefais gyfleoedd i ddiwallu fy nghanlyniadau / medrau dysgu tra 'roeddwn ar leoliad gwaith",
        "en": "I was given opportunities to meet my required practice learning outcomes/competences"
    },
    "important_you_need_to_check_the_details_of_any_courses_you_are_considering_or_applying_for_on_the_university_or_college_website": {
        "cy": "Pwysig: Mae angen i chi wirio manylion unrhyw cwrs yr ydych yn ystyried neu ceisio amdani ar wefan y prifysgol neu coleg. ",
        "en": "Important: You need to check the details of any courses you are considering or applying for on the university or college website."
    },
    "info_advice": {
        "cy": "Gwybodaeth a chyngor",
        "en": "Info and advice"
    },
    "info_and_advice": {
        "cy": "Gwybodaeth a chyngor",
        "en": "Information and advice."
    },
    "info_and_advice_url": {
        "cy": "/cy/how-choose-course-cy/",
        "en": "/how-do-i-choose-course/"
    },
    "info_n_advice": {
        "cy": "Gwybodaeth a chyngor",
        "en": "Information and advice"
    },
    "information_advice": {
        "cy": "Ewch i <strong class=\"blue-text\">Gwybodaeth a chyngor</strong>",
        "en": "Go to <strong class=\"blue-text\">Information and advice</strong>"
    },
    "insta_link": {
        "cy": "Dolen Instagram",
        "en": "Instagram link"
    },
    "institution": {
        "cy": "Sefydliad",
        "en": "Institution"
    },
    "institution_az": {
        "cy": "Sefydliad A-Z",
        "en": "Institution A-Z"
    },
    "institution_name": {
        "cy": "Enw'r sefydliad",
        "en": "Institution name"
    },
    "institution_search_input": {
        "cy": "Mewnbwn chwilio sefydliad",
        "en": "Institution Search Input"
    },
    "internal_error": {
        "cy": "Roedd gwall wrth lwytho’r dudalen",
        "en": "There was an error loading the page"
    },
    "it_is_clear_how_students_feedback_on_the_course_has_been_acted_on": {
        "cy": "Mae’n glir sut gweithredwyd fel ymateb i adborth y myfyrwyr ar y cwrs",
        "en": "It is clear how students' feedback on the course has been acted on"
    },
    "learning": {
        "cy": "Dysgu",
        "en": "Learning"
    },
    "learning_and_teaching_methods": {
        "cy": "Dull addysgu'r cwrs",
        "en": "How the course is taught"
    },
    "left_lower_qualification": {
        "cy": "Wedi gadael gyda chymhwyster is",
        "en": "Have left with a lower qualification"
    },
    "left_no_qualification": {
        "cy": "Wedi gadael heb gymhwyster",
        "en": "Have left without a qualification"
    },
    "length": {
        "cy": "Hyd",
        "en": "Length"
    },
    "location": {
        "cy": "Lleoliad",
        "en": "Location"
    },
    "locations": {
        "cy": "Lleoliadau",
        "en": "Locations"
    },
    "managers_and_proprieters_in_agriculture_and_services": {
        "cy": "Rheolwyr a pherchnogion mewn amaethyddiaeth a gwasanaethau amaethyddol",
        "en": "Managers and proprieters in agriculture and services"
    },
    "many_courses_due_to_start_in_autumn_2020_are_being_changed_to_online_delivery_in_whole_or_part_start_dates_and_course_contentstructures_may_also_be_changing": {
        "cy": "Mae nifer o gyrsiau sydd fod dechrau yn ystod hydref 2020 yn cael eu newid i gyrsiau ar-lein naill ai’n gyfan gwbl neu’n rhan-amser, gall bod newidiau hefyd i ddiwrnodau cychwyn a cynnwys/strwythyr cyrsiau.",
        "en": "Many courses due to start in autumn 2020 are being changed to online delivery in whole or part. Start dates and course content/structures may also be changing."
    },
    "marking_and_assessment_has_been_fair": {
        "cy": "Mae’r marcio a’r asesu wedi bod yn deg",
        "en": "Marking and assessment has been fair"
    },
    "miles": {
        "cy": "milltiroedd",
        "en": "miles"
    },
    "more_pages_after": {
        "cy": "Mwy o dudalennau ar gael ar ôl",
        "en": "More pages available after"
    },
    "more_pages_before": {
        "cy": "Mwy o dudalennau ar gael cyn ",
        "en": "More pages available before"
    },
    "my_contribution_during_placements_as_part_of_a_clinical_team_was_valued": {
        "cy": "Gosodwyd gwerth ar fy nghyfraniad fel rhan o'r tîm clinigol yn ystod fy lleoliad(au) gwaith",
        "en": "My contribution during placement(s) as part of a clinical team was valued"
    },
    "my_course_has_challenged_me_to_achieve_my_best_work": {
        "cy": "Mae fy nghwrs wedi fy herio i i wneud fy ngwaith gorau",
        "en": "My course has challenged me to achieve my best work"
    },
    "my_course_has_provided_me_with_opportunities_to_apply_what_i_have_learnt": {
        "cy": "Mae fy nghwrs wedi rhoi cyfleoedd i mi i ddefnyddio’r hyn rydw i wedi’i ddysgu",
        "en": "My course has provided me with opportunities to apply what I have learnt"
    },
    "my_course_has_provided_me_with_opportunities_to_bring_information_and_ideas_together_from_different_topics": {
        "cy": "Mae fy nghwrs wedi rhoi cyfleoedd i mi i ddod â gwybodaeth a syniadau at ei gilydd o wahanol bynciau",
        "en": "My course has provided me with opportunities to bring information and ideas together from different topics"
    },
    "my_course_has_provided_me_with_opportunities_to_explore_ideas_or_concepts_in_depth": {
        "cy": "Mae fy nghwrs wedi rhoi cyfleoedd i mi i archwilio syniadau neu gysyniadau’n fanwl",
        "en": "My course has provided me with opportunities to explore ideas or concepts in depth"
    },
    "my_practice_supervisors_understood_how_my_placements_related_to_the_broader_requirements_of_my_course": {
        "cy": "Roedd fy ngoruchwyliwr yn ystod fy nghyfnod ymarfer yn deall sut 'roedd fy lleoliad(au) gwaith yn perthyn i ofynion ehangach fy nghwrs",
        "en": "My practice supervisor(s) understood how my placement(s) related to the broader requirements of my course"
    },
    "n_courses_bookmarked_pt_1": {
        "cy": "Mae gennych",
        "en": "You have"
    },
    "n_courses_bookmarked_pt_2": {
        "cy": "o gyrsiau wedi'u nodi",
        "en": "courses bookmarked"
    },
    "narrow_location": {
        "cy": "Hidlo yn ôl lleoliad",
        "en": "Narrow location"
    },
    "national_student_survey": {
        "cy": "ACF (Arolwg Cenedlaethol o Fyfyrwyr)",
        "en": "NSS (National Student Survey)"
    },
    "near_your_home": {
        "cy": "agos at adref",
        "en": "to near your home"
    },
    "need_help_choosing": {
        "cy": "Angen cymorth i ddewis?",
        "en": "Need help choosing?"
    },
    "new_search": {
        "cy": "Chwiliad newydd",
        "en": "New Search"
    },
    "next": {
        "cy": "Nesaf",
        "en": "Next"
    },
    "next_page": {
        "cy": "Y dudalen nesaf",
        "en": "Next page"
    },
    "no_courses_found": {
        "cy": "Ni chafwyd hyd i unrhyw gyrsiau - canslwch neu newidiwch rai hidlyddion",
        "en": "No courses found, remove or change some filters"
    },
    "no_courses_saved": {
        "cy": "Nid oes unrhyw gyrsiau wedi’u cadw. I gymharu cyrsiau, chwiliwch am gyrsiau sydd o ddiddordeb ichi a’u cadw.",
        "en": "No courses saved. To compare courses, search for and save courses you're interested in."
    },
    "no_courses_selected": {
        "cy": "Nid ydych wedi dewis unrhyw gyrsiau",
        "en": "No courses selected"
    },
    "no_qualifications": {
        "cy": "Dim cymwysterau blaenorol / cymwysterau anhysbys",
        "en": "No / unknown prior qualifications"
    },
    "no_results_found": {
        "cy": "Ni chafwyd canlyniad.",
        "en": "No results found"
    },
    "none_recorded": {
        "cy": "Ni chofnodwyd yr un",
        "en": "None recorded"
    },
    "northern_ireland": {
        "cy": "Gogledd Iwerddon",
        "en": "Northern Ireland"
    },
    "not_available": {
        "cy": "Ddim ar gael",
        "en": "Not Available"
    },
    "not_enough": {
        "cy": "Ychwanegwch un arall er mwyn cymharu cyrsiau",
        "en": "Add another to compare courses."
    },
    "not_found_looking": {
        "cy": "Heb ddarganfod yr hyn yr oedd ei angen arnoch?",
        "en": "Not found what you were looking for?"
    },
    "not_professional_or_managerial": {
        "cy": "Ddim mewn swydd broffesiynol neu reoli",
        "en": "Not in a professional or managerial job"
    },
    "now_working": {
        "cy": "Yn gweithio bellach",
        "en": "Now working"
    },
    "number_of_results": {
        "cy": "Ceir <strong>%s</strong> cwrs gan <strong>%s</strong> darparydd",
        "en": "<strong>%s</strong> course(s) from <strong>%s</strong> provider(s)"
    },
    "number_options_selected": {
        "cy": "Dewiswyd {} opsiwn",
        "en": "{} options selected"
    },
    "number_selected_institutions": {
        "cy": "Dewiswyd {} sefydliad",
        "en": "{} selected institutions"
    },
    "of_those_asked": {
        "cy": "or rhai y gofynnwyd iddynt",
        "en": "of those asked"
    },
    "on_campus": {
        "cy": "Ar y campws",
        "en": "On campus"
    },
    "optional": {
        "cy": "Dewisol",
        "en": "Optional"
    },
    "other": {
        "cy": "Arall ",
        "en": "Other"
    },
    "other_higher_qualifications": {
        "cy": "Cymhwyster addysg uwch gwahanol",
        "en": "Different higher education qualification"
    },
    "other_undergraduate": {
        "cy": "Isradd arall (e.e. tystysgrif, diploma, gradd sylfaen)",
        "en": "Other undergraduate (e.g. CertHE, DipHE, FD)"
    },
    "other_work": {
        "cy": "Mewn math arall o swydd",
        "en": "In other work"
    },
    "overall_i_am_satisfied_with_the_quality_of_the_course": {
        "cy": "Ar y cyfan, rydw i’n fodlon gydag ansawdd y cwrs",
        "en": "Overall, I am satisfied with the quality of the course"
    },
    "page_not_found": {
        "cy": "Nid yw’r cwrs hwn neu’r dudalen hon ar gael",
        "en": "This course or page is not available"
    },
    "part_time": {
        "cy": "Rhan-amser",
        "en": "Part time"
    },
    "people": {
        "cy": "o fyfyrwyr",
        "en": "people"
    },
    "placement_year": {
        "cy": "Blwyddyn ar leoliad",
        "en": "Placement year"
    },
    "postcode": {
        "cy": "Cod post",
        "en": "Postcode"
    },
    "previous_page": {
        "cy": "Y dudalen flaenorol",
        "en": "Previous page"
    },
    "professional_accreditation": {
        "cy": "Achrediad professiyno",
        "en": "Professional accreditation"
    },
    "professional_accreditation_no_data": {
        "cy": "Nid oes unrhyw achrediadau proffesiynol wedi'u cofnodi",
        "en": "There are no professional accreditations recorded"
    },
    "professional_or_managerial": {
        "cy": "Mewn swydd broffesiynol neu reoli",
        "en": "In a professional or managerial job"
    },
    "prov_pc_text_template_go": {
        "cy": "<div><p>Mae {}% o raddedigion {} yn {} sy’n preswylio yn y DU wedi'u cyflogi yn {}.</p></div>",
        "en": "<div><p>{}% of UK-resident {} graduates from {} are employed in {}.</p></div>"
    },
    "prov_pc_text_template_leo": {
        "cy": "<div><p>Mae {}% o raddedigion {} yn {} sy’n preswylio yn y DU wedi'u lleoli yn {}.</p></div>",
        "en": "<div><p>{}% of UK-resident {} graduates from {} are based in {}.</p></div>"
    },
    "provisional": {
        "cy": "Dros dro",
        "en": "Provisional"
    },
    "qualification_type": {
        "cy": "Math o gymhwyster",
        "en": "Qualification type"
    },
    "regions": {
        "cy": "Rhanbarth(au)",
        "en": "Region(s)"
    },
    "remove_course": {
        "cy": "Dileu cwrs",
        "en": "Remove course"
    },
    "remove_filters": {
        "cy": "Dileu yr holl hidlwyr",
        "en": "Remove all filters"
    },
    "remove_others": {
        "cy": "I ddileu cyrsiau, ewch i'r ",
        "en": "To remove courses go to"
    },
    "respondents": {
        "cy": "o myfyrwyr",
        "en": "students"
    },
    "results": {
        "cy": "Canlyniadau",
        "en": "Results"
    },
    "sandwich_year": {
        "cy": "Blwyddyn ryngosod",
        "en": "Sandwich year"
    },
    "save_courses": {
        "cy": "Cadw cyrsiau",
        "en": "Save courses"
    },
    "saved": {
        "cy": "Wedi’u cadw",
        "en": "Saved"
    },
    "saved_courses": {
        "cy": "Cyrsiau wedi’u cadw",
        "en": "Saved courses"
    },
    "scotland": {
        "cy": "Yr Alban",
        "en": "Scotland"
    },
    "scroll_to_the_right": {
        "cy": "Sgroliwch i’r dde",
        "en": "Scroll to the right"
    },
    "search": {
        "cy": "Chwilio",
        "en": "Search"
    },
    "search_again": {
        "cy": "Chwilio eto",
        "en": "Search again"
    },
    "search_by_course_or_institution": {
        "cy": "Chwilio yn ôl enw cwrs ac/neu sefydliad",
        "en": "Search by course name and/or institution"
    },
    "search_guidelines": {
        "cy": "Chwiliwch am gymorth yn ein canllawiau i wneud y penderfyniad gorau i chi.",
        "en": "Search our guidelines for help making the best decision for you."
    },
    "search_institutions": {
        "cy": "Chwilio am sefydliadau",
        "en": "Search institutions"
    },
    "search_n_compare": {
        "cy": "Chwilio a chymharu",
        "en": "Search and compare"
    },
    "search_our_guidance": {
        "cy": "Chwiliwch yn ein canllawiau am gymorth i wneud y penderfyniad gorau i chi.",
        "en": "Search our guidance for help making the best decision for you."
    },
    "search_results": {
        "cy": "Canlyniadau'r chwiliad",
        "en": "Search results"
    },
    "search_within": {
        "cy": "Chwilio yn ",
        "en": "Search within"
    },
    "see_courses": {
        "cy": "Gweld y cyrsiau",
        "en": "See courses"
    },
    "select_all": {
        "cy": "Dewis popeth sy'n berthnasol",
        "en": "Select all"
    },
    "select_all_institutions": {
        "cy": "Dewis pob sefydliad",
        "en": "Select all institutions"
    },
    "select_all_results": {
        "cy": "Dewis pob canlyniad",
        "en": "Select all results"
    },
    "select_at_least_2": {
        "cy": "Dewiswch o leiaf 2 gwrs i’w cymharu",
        "en": "Select at least 2 courses to compare"
    },
    "select_course": {
        "cy": "Dewis cwrs",
        "en": "Select a course"
    },
    "select_subject": {
        "cy": "Dewis Pwnc",
        "en": "Select Subject"
    },
    "select_up_to_7": {
        "cy": "Dewiswch hyd at 7 cwrs i’w cymharu",
        "en": "Select up to 7 courses to compare"
    },
    "selected_1": {
        "cy": "Dewiswyd",
        "en": ""
    },
    "selected_2": {
        "cy": "o",
        "en": "selected of"
    },
    "send_message": {
        "cy": "Anfon neges",
        "en": "Send message"
    },
    "show_all": {
        "cy": "Dangos popeth",
        "en": "Show all"
    },
    "show_data_from": {
        "cy": "Dangos data o",
        "en": "Show data from"
    },
    "show_filters": {
        "cy": "Dangoswch yr Hidlau",
        "en": "Show Filters"
    },
    "show_less": {
        "cy": "Dangos llai",
        "en": "Show less"
    },
    "show_more": {
        "cy": "Dangos mwy",
        "en": "Show more"
    },
    "silver": {
        "cy": "Arian",
        "en": "Silver"
    },
    "similar_courses_elsewhere": {
        "cy": "Gweld cyrsiau tebyg mewn prifysgolion  <strong>eraill</strong> ",
        "en": "View similar courses at <strong>other</strong> unis"
    },
    "similar_courses_here": {
        "cy": "Gweld cyrsiau tebyg yn y brifysgol <strong>hon</strong> ",
        "en": "View similar courses at <strong>this</strong> uni"
    },
    "site_logo": {
        "cy": "<strong>Darganfod</strong> y Brifysgol",
        "en": "<strong>Discover</strong> Uni"
    },
    "skip": {
        "cy": "anwybyddu",
        "en": "Skip"
    },
    "sort_by": {
        "cy": "Didoli yn ôl:",
        "en": "Sort by:"
    },
    "source": {
        "cy": "Ffynhonnell",
        "en": "Source"
    },
    "specific_town_city": {
        "cy": "i dref/ddinas benodol",
        "en": "to a specific town/city"
    },

    "specific_uni": {
        "cy": "i brifysgol benodol",
        "en": "to a specific uni"
    },
    "staff_are_good_at_explaining_things": {
        "cy": "Mae'r staff yn dda am esbonio pethau",
        "en": "Staff are good at explaining things"
    },
    "staff_have_made_the_subject_interesting": {
        "cy": "Mae'r staff wedi gwneud y pwnc yn ddiddorol",
        "en": "Staff have made the subject interesting"
    },
    "staff_value_students_views_and_opinions_about_the_course": {
        "cy": "Mae’r staff yn gwerthfawrogi barn a safbwynt y myfyrwyr am y cwrs",
        "en": "Staff value students' views and opinions about the course"
    },
    "start": {
        "cy": "Dechrau",
        "en": "Start"
    },
    "still_on_course": {
        "cy": "Yn dal i astudio",
        "en": "Are still studying"
    },
    "student_satisfaction_course_overview_1": {
        "cy": "Bodlonrwydd Myfyrwyr",
        "en": "Student Satisfaction"
    },
    "student_satisfaction_course_overview_2": {
        "cy": "cyfran y myfyrwyr a ymatebodd a oedd yn cytuno â’r datganiad “Rwy’n fodlon ag ansawdd y cwrs ar y cyfan”",
        "en": "agreed they were satisfied with the quality of the course"
    },
    "student_satisfaction_course_overview_3": {
        "cy": "Ewch i’r adran Bodlonrwydd Myfyrwyr",
        "en": "Go to Student Satisfaction"
    },
    "student_unions": {
        "cy": "Undebau Myfyrwyr",
        "en": "Student Unions"
    },
    "study_abroad_year": {
        "cy": "Blwyddyn dramor",
        "en": "Study abroad year"
    },
    "study_and_working": {
        "cy": "Gweithio a astudio",
        "en": "Working and studying"
    },
    "study_mode": {
        "cy": "Modd astudio",
        "en": "Study mode"
    },
    "subject": {
        "cy": "Pwnc ",
        "en": "Subject"
    },
    "subject_area": {
        "cy": "Maes pwnc",
        "en": "Subject area"
    },
    "subject_at_least_two": {
        "cy": "Pwnc (dewiswch o ddau neu fwy o'r blychau isod, os gwelwch yn dda)",
        "en": "Subject (please select from at least two of the boxes below)"
    },
    "subject_select_text": {
        "cy": "Mae gan rai cyrsiau a ddewisir ddata o fwy nag un pwnc. Dewiswch y pwnc rydych am weld data ohono",
        "en": "Some courses selected have data from more than one subject. Select the subject you wish to see data from."
    },
    "summary_med_sal_text_1": {
        "cy": "ar ôl y cwrs i raddedigion",
        "en": "after the course for"
    },
    "summary_med_sal_text_2": {
        "cy": "yn",
        "en": "graduates at"
    },
    "tariff_graph_desc": {
        "cy": " Nifer y myfyrwyr a ddechreuodd y cwrs gyda phwyntiau tariff yn yr ystod",
        "en": " of students entered the course with tariff points in range"
    },
    "tariff_graph_title": {
        "cy": "Graff yn dangos nifer y myfyrwyr yn dechrau’r cwrs gyda phwyntiau tariff yn yr ystod",
        "en": "Graph showing number of students entering the course with tariff points in range"
    },
    "telephone": {
        "cy": "Ffôn",
        "en": "Telephone"
    },
    "the_course_is_intellectually_stimulating": {
        "cy": "Mae'r cwrs yn symbylu'r deallusrwydd",
        "en": "The course is intellectually stimulating"
    },
    "the_course_is_well_organised_and_running_smoothly": {
        "cy": "Mae'r cwrs wedi’i drefnu'n dda ac mae'n rhedeg yn hwylus",
        "en": "The course is well organised and running smoothly"
    },
    "the_criteria_used_in_marking_have_been_clear_in_advance": {
        "cy": "Mae'r meini prawf a ddefnyddir ar gyfer marcio wedi cael eu gwneud yn eglur ymlaen llaw",
        "en": "The criteria used in marking have been clear in advance"
    },
    "the_it_resources_and_facilities_provided_have_supported_my_learning_well": {
        "cy": "Mae’r adnoddau a’r cyfleusterau TG sydd wedi’u darparu wedi cefnogi fy nysgu i’n dda",
        "en": "The IT resources and facilities provided have supported my learning well"
    },
    "the_library_resources_eg_books_online_services_and_learning_spaces_have_supported_my_learning_well": {
        "cy": "Mae’r adnoddau llyfrgell (e.e. llyfrau, gwasanaethau ar-lein a gofod dysgu) wedi cefnogi fy nysgu i’n dda",
        "en": "The library resources (e.g. books, online services and learning spaces) have supported my learning well"
    },
    "the_students_union_association_or_guild_effectively_represents_students_academic_interests": {
        "cy": "Mae undeb y myfyrwyr (cymdeithas neu urdd) yn cynrychioli buddiannau academaidd y myfyrwyr yn effeithiol",
        "en": "The students' union (association or guild) effectively represents students' academic interests"
    },
    "the_timetable_works_efficiently_for_me": {
        "cy": "Mae’r amserlen yn gweithio’n effeithlon i mi",
        "en": "The timetable works efficiently for me"
    },
    "try_course_wizard": {
        "cy": "Rhowch gynnig ar ein dewin cwrs er mwyn culhau eich chwiliad",
        "en": "Try our course wizard to narrow your search down"
    },
    "twitter_link": {
        "cy": "Dolen Twitter",
        "en": "Twitter link"
    },
    "typical_range": {
        "cy": "Ystod arfero",
        "en": "Typical range"
    },
    "under_courses_uk": {
        "cy": "cyrsiau israddedig yn y DU",
        "en": "undergraduate courses in the UK"
    },
    "unemp_not_work_since_grad": {
        "cy": "Yn ddi-waith - heb gael gwaith ers graddio",
        "en": "Unemployed - not employed since graduation"
    },
    "unemp_prev_emp_since_grad": {
        "cy": "Yn ddi-waith - yn gweithio neun astudio cyn hynny",
        "en": "Unemployed – previously working or studying"
    },
    "unemployed": {
        "cy": "Yn ddi-waith",
        "en": "Unemployed"
    },
    "uni_and_college": {
        "cy": "Pob prifysgol a choleg",
        "en": "All universities and colleges"
    },
    "uni_college": {
        "cy": "Brifysgolion / cholegau",
        "en": "Universities / colleges"
    },
    "unknown": {
        "cy": "Anhysbys",
        "en": "Unknown"
    },
    "unknown_job_type": {
        "cy": "Mewn swydd anhysbys",
        "en": "In an unknown job type"
    },
    "unknown_work": {
        "cy": "Mewn swydd anhysbys",
        "en": "In unknown work"
    },
    "video_on_topic_content": {
        "cy": "2 funud o hyd",
        "en": "2 mins long"
    },
    "video_on_topic_title": {
        "cy": "Fideo ar bwnc perthnasol",
        "en": "Video on a relevant topic"
    },
    "view_all_courses": {
        "cy": "Gweld pob cwrs y brifysgol hon",
        "en": "View all courses at this university/college"
    },
    "view_your_courses": {
        "cy": "Gweld eich cyrsiau",
        "en": "View your courses"
    },
    "wales": {
        "cy": "Cymru",
        "en": "Wales"
    },
    "website": {
        "cy": "Gwefan",
        "en": "Website"
    },
    "with_abroad": {
        "cy": "Gyda blwyddyn dramor",
        "en": "With year abroad"
    },
    "with_foundation": {
        "cy": "Gyda'r flwyddyn sylfaen",
        "en": "With foundation year"
    },
    "with_placement": {
        "cy": "Gyda blwyddyn leoliad",
        "en": "With placement year"
    },
    "withdrawn": {
        "cy": "Wedi galw’n ôl",
        "en": "Withdrawn"
    },
    "within_miles": {
        "cy": "fewn {} milltir",
        "en": "within {} miles"
    },
    "without_abroad": {
        "cy": "Heb flwyddyn dramor",
        "en": "Without year abroad"
    },
    "without_foundation": {
        "cy": "Heb flwyddyn sylfaen",
        "en": "Without foundation year"
    },
    "without_placement": {
        "cy": "Heb flwyddyn leoliad",
        "en": "Without placement year"
    },
    "work_placement_year": {
        "cy": "Blwyddyn lleoliad gwaith",
        "en": "Work placement year"
    },
    "year": {
        "cy": "blynedd",
        "en": "year"
    },
    "year_abroad": {
        "cy": "Blwyddyn dramor",
        "en": "Year abroad"
    },
    "year_course": {
        "cy": "blwyddyn",
        "en": "year course"
    },
    "years": {
        "cy": "mlynedd",
        "en": "years"
    },
    "yes": {
        "cy": "Ydy",
        "en": "Yes"
    },
    "you_can": {
        "cy": "Gallwch ",
        "en": "You can"
    },
    "youre_interested_in": {
        "cy": "sydd o ddiddordeb iti",
        "en": "you're interested in"
    },

    'data_need_to_know': {
        'en': 'What you need to know about the data',
        'cy': "Beth sydd angen i chi ei wybod ynglŷn â'r data"
    },
    "data_need_to_know_2": {
        "cy": "Beth sydd angen i chi ei wybod ynglŷn â’r data hwn",
        "en": "What you need to know about this data"
    },
    'employment_need_to_know': {
        'en': 'What you need to know about employment data',
        'cy': 'Beth sydd angen i chi ei wybod ynglŷn â data cyflogaeth'
    },
    'survey_need_to_know': {
        'en': 'What you need to know about the student survey data',
        'cy': "Beth sydd angen i chi ei wybod ynglŷn â data'r arolwg o fyfyrwyr"
    },
    "earnings_need_to_know": {
        "cy": "Beth sydd angen i chi ei wybod ynglŷn â data enillion",
        "en": "What you need to know about earnings data"
    },

    'student_satisfaction_info_box': {
        'cy': "<li>Mae'r data gan fyfyrwyr a arolygwyd yn ystod y pandemig COVID-19.  </li>"
              "<li>Effeithiwyd ar rai cyrsiau a darparwyr yn fwy nag eraill.</li>"
              "<li>Mae'r data yn dweud wrthych am brofiad myfyrwyr diweddar, ond gallai eich profiad chi fod yn wahanol.</li>",
        'en': '<li>The data is from students surveyed during the Covid-19 pandemic.</li>'
              '<li>Some courses and providers have been affected more than others.</li>'
              '<li>The data tells you about the experience of recent students, but your experience may be different.</li>'

    },

    "earnings_info_box": {
        "cy": "<li>Mae rhywfaint o ddata gan raddedigion a arolygwyd yn ystod y pandemig COVID-19.</li>"
              "<li>Mae marchnadoedd llafur yn newid.</li>"
              "<li>Mae cyflogau yn amrywio ar draws rhanbarthau yn y DU. Mae cyflogau yn amrywio ar draws rhanbarthau yn y DU.</li>"
              "<li<Mae yna lawer o ffactorau sy'n effeithio ar enillion graddedigion.</li>",
        "en": "<li>Some data is from graduates surveyed during the Covid-19 pandemic.</li>"
              "<li>Labour markets change </li>"
              "<li>Salaries vary across regions in the UK</li>"
              "<li>There are lots of factors that affect graduate earnings.</li>"
    },

    'graduate_perceptions_info_box': {
        'en': '<li>Some data is from graduates surveyed during the Covid-19 pandemic</li>',
        'cy': '<li>Mae rhywfaint o ddata gan raddedigion a arolygwyd yn ystod y pandemig COVID-19.</li>'
    },
    'employment_info_box': {
        'en': '<li>Some data is from graduates surveyed during Covid-19 pandemic</li>'
              '<li>Labour markets vary and change over time</li>'
              '<li>Employment and job opportunities vary across regions in the UK</li>',
        'cy': '<li>Mae rhywfaint o ddata gan raddedigion a arolygwyd yn ystod y pandemig COVID-19.</li>'
              '<li>Mae marchnadoedd llafur yn amrywio ac yn newid dros amser.</li>'
              '<li>Mae cyfleoedd cyflogaeth a swyddi yn amrywio ar draws rhanbarthau yn y DU.</li>'
    },
    'survey_info_box': {
        'en': 'Student satisfation data is from the 2021 NSS survey and many have been affected by the Covid-19 pandemic.',
        'cy': "Mae rhywfaint o'r data gan fyfyrwyr a arolygwyd yn ystod y pandemig COVID-19, a allai fod wedi cael effaith ar eu hymatebion."
    },
}
