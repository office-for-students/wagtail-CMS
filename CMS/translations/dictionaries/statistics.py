def dict_for_key(english, welsh):
    return dict(en=english, cy=welsh)


UNAVAILABLE = {
    "earnings_15_months_unavailable_22_21_3": dict_for_key(
        "This includes data from this and related courses at the same university or college. There was not enough data to publish more specific information. This does not reflect on the quality of the course.",
        "Mae hwn yn cynnwys data o'r cwrs hwn a chyrsiau cysylltiedig yn yr un brifysgol neu goleg. Nid oedd digon o ddata ar gael i gyhoeddi gwybodaeth fwy manwl. Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    ),
    "earnings_15_months_unavailable_22_21_4": dict_for_key(
        "<p>This includes data from this and related courses at the same university or college. There was not enough data to publish more specific information. This does not reflect on the quality of the course.</p><p>Please note: the following information does not contain any data for first degrees (such as BA, BSc, or Integrated Masters). Instead it is displaying information for other undergraduate qualifications – this includes CertHE, DipHE and FD among others.</p>",
        "<p>Mae hwn yn cynnwys data o'r cwrs hwn a chyrsiau cysylltiedig yn yr un brifysgol neu goleg. Nid oedd digon o ddata ar gael i gyhoeddi gwybodaeth fwy manwl. Nid yw hyn yn adlewyrchu ansawdd y cwrs.</p><p>Sylwch: nid yw'r wybodaeth ganlynol yn cynnwys unrhyw ddata ar gyfer graddau cyntaf (fel BA, BSc neu Gwrs Meistr Integredig). Yn lle hynny, mae'n dangos gwybodaeth ar gyfer cymwysterau israddedig eraill - mae hyn yn cynnwys Tystysgrif Addysg Uwch, Diploma Addysg Uwch a Gradd Sylfaen ymhlith eraill.</p>"
    ),
    "earnings_15_months_unavailable_0_any": dict_for_key(
        "This is either because the course size is small or there were not enough responses to produce data. This does not reflect on the quality of the course.",
        "Mae hyn naill ai oherwydd bod y cwrs yn fach neu am nad oedd digon o ymatebion ar gael i gynhyrchu data. Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    ),
    "earnings_15_months_unavailable_1_any": dict_for_key(
        "This is because the course has not yet run or has not been running long enough for this data to be available.",
        "Mae hyn oherwydd nad yw'r cwrs wedi'i gynnal eto neu nad yw wedi cael ei gynnal yn ddigon hir i’r data hyn fod ar gael."
    ),
    "earnings_15_months_unavailable_2_any": dict_for_key(
        "This does not reflect on the quality of the course.",
        "Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    )
}

STATISTICS = {
    "entry_information": dict_for_key("Entry Information", "Gwybodaeth am fynediad"),
    "earnings_after_the_course": dict_for_key("Earnings after the course", "Enillion ar ôl y cwrs"),
    "employment_15_months": dict_for_key("Employment 15 months after the course", "Cyflogaeth 15 mis ar ôl y cwrs"),
    "graduate_perceptions": dict_for_key("Graduate perceptions", "Canfyddiadau graddedigion"),
    "information_on_uni": dict_for_key("Information on the uni website", "Gwybodaeth ar wefan y prifysgol"),
    'overall_satisfied': {
        'en': 'Overall I am satisfied with the quality of the course',
        'cy': 'Rwy’n fodlon ag ansawdd y cwrs ar y cyfan'
    },
    'data_from_people': {
        'en': 'Data from (# of people)',
        'cy': "Data gan (# o fyfyrwyr)"
    },
    'percent_of_those_asked': {
        'en': '% of those asked',
        'cy': "% o'r rhai y gofynnwyd iddynt"
    },
    'teaching_on_my_course': {
        'en': 'Teaching on my course',
        'cy': 'Yr addysgu ar fy nghwrs'
    },
    'learning_opportunities': {
        'en': "Learning opportunities",
        'cy': "Cyfleoedd dysgu"
    },
    'assessment_and_feedback': {
        'en': "Assessment and feedback",
        'cy': "Asesiad ac adborth"
    },
    'academic_support': {
        'en': "Academic support",
        'cy': "Cefnogaeth academaidd"
    },
    'organisation_and_management': {
        'en': "Organisation and management",
        'cy': "Trefniant a rheolaeth"
    },
    'learning_resources': {
        'en': "Learning resources",
        'cy': "Adnoddau dysgu"
    },
    'learning_community': {
        'en': "Learning community",
        'cy': "Cymuned ddysgu"
    },
    'student_voice': {
        'en': "Student voice",
        'cy': "Llais y myfyriwr"
    },
    'nss_question_1': {
        'en': "Staff are good at explaining things",
        'cy': "Mae'r staff yn dda am esbonio pethau"
    },
    'nss_question_2': {
        'en': "Staff have made the subject interesting.",
        'cy': "Mae'r staff wedi gwneud y pwnc yn ddiddorol"
    },
    'nss_question_3': {
        'en': "The course is intellectually stimulating.",
        'cy': "Mae'r cwrs yn symbylu'r deallusrwydd"
    },
    'nss_question_4': {
        'en': "My course has challenged me to achieve my best work.",
        'cy': "Mae fy nghwrs wedi fy herio i i wneud fy ngwaith gorau"
    },
    'nss_question_5': {
        'en': "My course has provided me with opportunities to explore ideas or concepts in depth.",
        'cy': "Mae fy nghwrs wedi rhoi cyfleoedd i mi i archwilio syniadau neu gysyniadau’n fanwl"
    },
    'nss_question_6': {
        'en': "My course has provided me with opportunities to bring information and ideas together from different topics.",
        'cy': "Mae fy nghwrs wedi rhoi cyfleoedd i mi i ddod â gwybodaeth a syniadau at ei gilydd o wahanol bynciau"
    },
    'nss_question_7': {
        'en': "My course has provided me with opportunities to apply what I have learnt.",
        'cy': "Mae fy nghwrs wedi rhoi cyfleoedd i mi i ddefnyddio’r hyn rydw i wedi’i ddysgu"
    },
    'nss_question_8': {
        'en': "The criteria used in marking have been clear in advance.",
        'cy': "Mae'r meini prawf a ddefnyddir ar gyfer marcio wedi cael eu gwneud yn eglur ymlaen llaw"
    },
    'nss_question_9': {
        'en': "Marking and assessment has been fair.",
        'cy': "Mae’r marcio a’r asesu wedi bod yn deg"
    },
    'nss_question_10': {
        'en': "Feedback on my work has been timely.",
        'cy': "Mae’r adborth ar fy ngwaith i wedi bod yn amserol"
    },
    'nss_question_11': {
        'en': "I have received helpful comments on my work.",
        'cy': "Rydw i wedi cael sylwadau defnyddiol ar fy ngwaith"
    },
    'nss_question_12': {
        'en': "I have been able to contact staff when I needed to.",
        'cy': "Rydw i wedi gallu cysylltu â staff pan oeddwn i angen gwneud hynny"
    },
    'nss_question_13': {
        'en': "I have received sufficient advice and guidance in relation to my course.",
        'cy': "Rydw i wedi cael digon o gyngor ac arweiniad mewn perthynas â'm cwrs"
    },
    'nss_question_14': {
        'en': "Good advice was available when I needed to make study choices on my course.",
        'cy': "Roedd cyngor da ar gael i mi pan oeddwn i eisiau gwneud dewisiadau astudio ar fy nghwrs"
    },
    'nss_question_15': {
        'en': "The course is well organised and is running smoothly.",
        'cy': "Mae'r cwrs wedi’i drefnu'n dda ac mae'n rhedeg yn hwylus"
    },
    'nss_question_16': {
        'en': "The timetable works efficiently for me.",
        'cy': "Mae’r amserlen yn gweithio’n effeithlon i mi"
    },
    'nss_question_17': {
        'en': "Any changes in the course or teaching have been communicated effectively.",
        'cy': "Cafwyd cyfathrebu effeithiol ynghylch unrhyw newidiadau o ran y cwrs neu'r addysgu"
    },
    'nss_question_18': {
        'en': "The IT resources and facilities provided have supported my learning well.",
        'cy': "Mae’r adnoddau a’r cyfleusterau TG sydd wedi’u darparu wedi cefnogi fy nysgu i’n dda"
    },
    'nss_question_19': {
        'en': "The library resources (e.g. books, online services and learning spaces) have supported my learning well.",
        'cy': "Mae’r adnoddau llyfrgell (e.e. llyfrau, gwasanaethau ar-lein a gofod dysgu) wedi cefnogi fy nysgu i’n dda"
    },
    'nss_question_20': {
        'en': "I have been able to access course-specific resources (e.g. equipment, facilities, software, collections) when I needed to.",
        'cy': "Rydw i wedi gallu cael mynediad at adnoddau penodol i gwrs (e.e. offer, cyfleusterau, meddalwedd, casgliadau) pan oedd angen i mi wneud hynny"
    },
    'nss_question_21': {
        'en': "I feel part of a community of staff and students.",
        'cy': "Rydw i’n teimlo’n rhan o gymuned o staff a myfyrwyr"
    },
    'nss_question_22': {
        'en': "I have had the right opportunities to work with other students as part of my course.",
        'cy': "Rydw i wedi cael cyfleoedd priodol i weithio gyda myfyrwyr eraill fel rhan o'm cwrs"
    },
    'nss_question_23': {
        'en': "I have had the right opportunities to provide feedback on my course.",
        'cy': "Rydw i wedi cael cyfleoedd priodol i roi adborth ar fy nghwrs"
    },
    'nss_question_24': {
        'en': "Staff value students’ views and opinions about the course.",
        'cy': "Mae’r staff yn gwerthfawrogi barn a safbwynt y myfyrwyr am y cwrs"
    },
    'nss_question_25': {
        'en': "It is clear how students’ feedback on the course has been acted on.",
        'cy': "Mae’n glir sut gweithredwyd fel ymateb i adborth y myfyrwyr ar y cwrs"
    },
    'nss_question_26': {
        'en': "The students’ union (association or guild) effectively represents students’ academic interests.",
        'cy': "Mae undeb y myfyrwyr (cymdeithas neu urdd) yn cynrychioli buddiannau academaidd y myfyrwyr yn effeithiol"
    },
    'after_one_year': {
        'en': "After 1 year on the course",
        'cy': "Ar ôl blwyddyn o astudio"
    },
    'find_out_more_link': {
        'en': "https://www.discoveruni.gov.uk/about-our-data/",
        'cy': "https://www.discoveruni.gov.uk/cy/yngl%C5%B7n-%C3%A2n-data-about-our-data-cy/"
    },
    'satisfaction_guidance_1': {
        'en': '''<strong>Number of people the data is based on</strong> - 
            more people mean it is more likely giving a clearer picture of student experience. 
            Also consider the percentage of students who responded to the survey.''',
        'cy': '''<strong>Nifer y bobl y mae'r data'n seiliedig arnynt</strong> - 
            bydd mwy o bobl yn golygu ei bod hi'n debygol y ceir darlun cliriach o brofiadau myfyrwyr. 
            Dylech hefyd ystyried canran y myfyrwyr a ymatebodd i'r arolwg.'''
    },
    'satisfaction_guidance_2': {
        'en': '''<strong>Some data may be for a course and some for a subject</strong> -
            course data is more specific but subject data will still give an indication of students’ views. 
            Use caution when comparing the two.''',
        'cy': '''<strong>Gall rhywfaint o ddata fod ar gyfer cwrs a rhywfaint ar gyfer pwnc</strong> - 
            mae data cwrs yn fwy penodol ond bydd data pwnc yn dal i roi syniad o farn myfyrwyr. 
            Byddwch yn ofalus wrth gymharu'r naill a'r llall. 
            Darllenwch fwy am Arolwg Cenedlaethol o Fyfyrwyr'''
    },
    'read_more_about_satisfaction': {
        'en': "Read more about the National Student Survey",
        'cy': "Darllenwch fwy am Arolwg Cenedlaethol o Fyfyrwyr"
    },
    'after_one_year_guidance': {
        'en': '''The number of students indicates the size of the course, and more people 
            means it is more likely to be representative of outcomes for students.''',
        'cy': '''Bydd nifer y myfyrwyr yn dynodi maint y cwrs, ac os ceir mwy o bobl mae 
            hynny'n golygu ei fod yn fwy tebygol o gynrychioli canlyniadau myfyrwyr.'''
    },
    'read_more_about_continuation': {
        'en': "Read more about Continuation",
        'cy': "Darllenwch fwy am Parhad"
    },
    'employment_guidance_1': {
        'en': "Some data is from graduates surveyed during the pandemic",
        'cy': "Daw rhywfaint o ddata gan raddedigion a gymerodd ran yn yr arolwg yn ystod y pandemig."
    },
    'employment_guidance_2': {
        'en': "Labour markets vary and change over time",
        'cy': "Bydd marchnadoedd llafur yn amrywio ac yn newid dros amser"
    },
    'employment_guidance_3': {
        'en': "Employment and job opportunities vary across regions in the UK",
        'cy': "Bydd cyfleoedd am gyflogaeth a swyddi'n amrywio ar draws rhanbarthau'r DU"
    },
    'read_more_about_employment': {
        'en': "Read more about employment",
        'cy': "Darllen mwy am gyflogaeth"
    },
    'employment_link': {
        'en': "https://www.discoveruni.gov.uk/how-do-i-choose-course/employment-prospects/",
        'cy': "https://www.discoveruni.gov.uk/cy/how-choose-course-cy/rhagolygon-cyflogaeth-employment-prospects/"
    },
    'graduate_guidance_1': {
        'en': "Number of people the data is based on - more people mean it is more likely giving a clearer picture of student experience. Also consider the percentage of graduates who responded to the survey.",
        'cy': "Nifer y bobl y mae'r data'n seiliedig arnynt - bydd mwy o bobl yn golygu ei bod hi'n debygol y ceir darlun cliriach o brofiadau myfyrwyr. Dylech hefyd ystyried canran y myfyrwyr a ymatebodd i'r arolwg."
    },
    'graduate_guidance_2': {
        'en': "Some data may be for a course and some for a subject - course data is more specific but subject data will still give an indication of students’ views. Use caution when comparing the two.",
        'cy': "Gall rhywfaint o ddata fod ar gyfer cwrs a rhywfaint ar gyfer pwnc - mae data cwrs yn fwy penodol ond bydd data pwnc yn dal i roi syniad o farn myfyrwyr. Byddwch yn ofalus wrth gymharu'r naill a'r llall."
    },
    'read_more_about_graduate_perceptions': {
        'en': "Read more about Graduate Perceptions",
        'cy': "Darllenwch fwy am Canfyddiadau Graddedigion"
    },
    'graduate_link': {
        'en': "https://www.discoveruni.gov.uk/about-our-data/#graduate_outcomes_survey",
        'cy': "https://discoveruni.gov.uk/cy/yngl%C5%B7n-%C3%A2n-data-about-our-data-cy/#arolwg_canlyniadau_graddedigion"
    },
    'earnings_guidance_1': {
        'en': "Labour markets change",
        'cy': "mae marchnadoedd llaffur yn newid"
    },
    'earnings_guidance_2': {
        'en': "Salaries vary across regions in the UK",
        'cy': "mae cyflogau'n amrywio yng ngwahanol rannau o'r DU"
    },
    'earnings_guidance_3': {
        'en': "There are lots of factors that affect graduates' earnings",
        'cy': "mae llawer o ffactorau'n effeithio ar enillion graddedigion"
    },
    'read_more_about_earnings': {
        'en': "Read more about earnings",
        'cy': "Darllen mwy am enillion"
    },
    'earnings_link': {
        'en': "https://www.discoveruni.gov.uk/how-do-i-choose-course/employment-prospects/",
        'cy': "https://www.discoveruni.gov.uk/cy/how-choose-course-cy/rhagolygon-cyflogaeth-employment-prospects/"
    },
    'entry_guidance': {
        'en': "These are the qualifications students had when they were accepted onto this course. This is not a list of qualifications a person needs to have to be accepted onto this course",
        'cy': "Dyma'r cymwysterau a oedd gan fyfywyr wrth gael eu derbyn ar y cwrs yma. Nid rhestr o gymwysterau sydd eu hangen ar rywun er mwyn cael eu derbyn ar y cwrs yw hon"
    },
    'read_more_about_entry': {
        'en': "Read more about entry data",
        'cy': "Darllen mwy am ddata mynediad"
    },
    'employment_after_the_course': {
        'en': "What graduates are doing 15 months after the course",
        'cy': "Yr hyn y mae graddedigion yn ei wneud 15 mis ar y cwrs"
    },
    'occupation_type': {
        'en': "Occupation types 15 months after the course",
        'cy': "Mathau o swydd 15 mis ar ôl y cwrs"
    },
    'employed_in_professional': {
        'en': "Employed in a professional or managerial job",
        'cy': "Canran y rhai a gyflogir sydd mewn swydd broffesiynol neu swydd reoli ar ôl gorffen y cwrs."
    },
    'employed_not_in_professional': {
        'en': "Employed not in a professional or managerial job",
        'cy': "Canran y rhai a gyflogir nad ydynt mewn swydd broffesiynol neu swydd reoli ar gorffen y cwrs."
    },
    'usefulness': {
        'en': "Usefulness",
        'cy': "Pa mor ddefnyddiol"
    },
    'usefulness_subtitle': {
        'en': "I am utilising what I learnt during my studies in my current work.",
        'cy': "Rwy'n defnyddio'r hyn a ddysgais wrth astudio yn fy ngwaith presennol."
    },
    'meaningfulness': {
        'en': "Meaningfulness",
        'cy': "Pa mor ystyrlon"
    },
    'meaningfulness_subtitle': {
        'en': "My current work is meaningful.",
        'cy': "Mae fy ngwaith presennol yn ystyrlon."
    },
    'future': {
        'en': "Future",
        'cy': "Y Dyfodol"
    },
    'future_subtitle': {
        'en': " My current work fits with my future plans.",
        'cy': "Mae fy ngwaith presennol yn cyd-fynd â'm cynlluniau ar gyfer y dyfodol."
    },
    'no_data_available': {
        'en': "No data available",
        'cy': "Nid yw'r data ar gael"
    },
    'national_average': {
        'en': "National average",
        'cy': "Cyfartaledd cenedlaethol"
    },
    'after_15_months': {
        'en': "After 15 months",
        'cy': "Ar ôl 15 mis"
    },
    'after_3_years': {
        'en': "After 3 years",
        'cy': "Ar ôl 3 blynedd"
    },
    'after_5_years': {
        'en': "After 5 years",
        'cy': "Ar ôl 5 blynedd"
    },
    'unavailable_data_message': {
        'en': "This may be because the course size is too small or not enough students responded to the survey. This does not reflect on the quality of the course.",
        'cy': "Gall hyn fod oherwydd bod maint y cwrs yn rhy fach. Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    },
    'ucas_tariff_points': {
        'en': "UCAS Tariff points",
        'cy': "Pwyntiau Tariff UCAS"
    },
}
