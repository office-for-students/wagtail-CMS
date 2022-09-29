def dict_for_key(english, welsh, subject=None):
    return dict(en=english, cy=welsh)


UNAVAILABLE = {
    "new_course_agg_blank_header": {
        "en": "Sorry, there is no data available for this course.",
        "cy": "Mae’n ddrwg gennym, nid oes data ar gael ar gyfer y cwrs yma."
    },
    "new_course_agg_blank_body": {
        "en": "This is because the course is new or has not been running long enough for this data to be available. This does not reflect on the quality of the course.",
        "cy": "Y rheswm dros hyn yw bod y cwrs yn newydd neu nad yw wedi bod yn rhedeg am yn ddigon hir i’r data hwn fod ar gael. Nid yw hyn yn adlewyrchu ar ansawdd y cwrs."
    },
    "new_course_earnings_unavail_header": {
        "en": "The data displayed is from students on courses in {}.",
        "cy": "Daw'r data a ddangosir gan fyfyrwyr ar gyrsiau {}."
    },
    "new_course_earnings_unavail_body": {
        "en": "This includes data from all courses in this subject at the same university or college. There was not enough data to publish more specific information – either because the course is new, or there are too few students. This does not reflect on the quality of the course.",
        "cy": "Mae hwn yn cynnwys data o bob cwrs yn y pwnc hwn yn yr un brifysgol neu goleg. Nid oedd digon o ddata ar gael i gyhoeddi gwybodaeth fwy manwl - naill ai gan fod y cwrs yn newydd, neu does dim digon o fyfyrwyr. Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    },
    "new_course_unavail_full": dict_for_key(
        "The data displayed is from students on courses in {}. This includes data from all courses in this subject at the same university or college. There was not enough data to publish more specific information – either because the course is new, or there are too few students. This does not reflect on the quality of the course.",
        "Daw'r data a ddangosir gan fyfyrwyr ar gyrsiau {}. Mae hwn yn cynnwys data o bob cwrs yn y pwnc hwn yn yr un brifysgol neu goleg. Nid oedd digon o ddata ar gael i gyhoeddi gwybodaeth fwy manwl - naill ai gan fod y cwrs yn newydd, neu does dim digon o fyfyrwyr. Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    ),
    "new_course_agg_111213_header": {
        "en": "The data displayed is from students on other courses in {}.",
        "cy": "Mae’r data a ddangosir gan fyfyrwyr eraill ar gyrsiau eraill mewn {}."
    },
    "new_course_agg_111213_body": {
        "en": "Because the course is new or has not been running long enough, there was not enough data to publish information specifically for this course. This does not reflect on the quality of the course.",
        "cy": "Gan bod y cwrs yn newydd neu heb fod yn rhedeg am yn ddigon hir, nid oedd digon o ddata i gyhoeddi gwybodaeth ar gyfer y cwrs yma’n benodol. Nid yw hyn yn adlewyrchu ar ansawdd y cwrs."
    },
    "new_course_agg_212223_header": {
        "en": "The data displayed is from students on other courses in {} over the previous two years.",
        "cy": "Mae’r data a ddangosir gan fyfyrwyr ar gyrsiau eraill mewn {} dros y ddwy flynedd flaenorol."
    },
    "new_course_agg_212223_body": {
        "en": "Because the course is new or has not been running long enough, there was   not enough data to publish information specifically for this course.",
        "cy": "Gan bod y cwrs yn newydd neu heb fod yn rhedeg am yn ddigon hir, nid oedd digon o ddata i gyhoeddi gwybodaeth ar gyfer y cwrs yma’n benodol."
    },
    "after_5_years_21_22_4": dict_for_key(
        "<p>This includes data from this and related courses at the same university or college. There was not enough data to publish more specific information. This does not reflect on the quality of the course.</p><p>Please note: the following information does not contain any data for first degrees (such as BA, BSc, or Integrated Masters). Instead it is displaying information for other undergraduate qualifications – this includes CertHE, DipHE and FD among others.</p>",
        "<p>Mae hwn yn cynnwys data o'r cwrs hwn a chyrsiau cysylltiedig yn yr un brifysgol neu goleg. Nid oedd digon o ddata ar gael i gyhoeddi gwybodaeth fwy manwl. Nid yw hyn yn adlewyrchu ansawdd y cwrs.</p><p>Sylwch: nid yw'r wybodaeth ganlynol yn cynnwys unrhyw ddata ar gyfer graddau cyntaf (fel BA, BSc neu Gwrs Meistr Integredig). Yn lle hynny, mae'n dangos gwybodaeth ar gyfer cymwysterau israddedig eraill - mae hyn yn cynnwys Tystysgrif Addysg Uwch, Diploma Addysg Uwch a Gradd Sylfaen ymhlith eraill.</p>"
    ),
    "after_5_years_21_22_3": dict_for_key(
        "This includes data from this and related courses at the same university or college. There was not enough data to publish more specific information. This does not reflect on the quality of the course.",
        "Mae hwn yn cynnwys data o'r cwrs hwn a chyrsiau cysylltiedig yn yr un brifysgol neu goleg. Nid oedd digon o ddata ar gael i gyhoeddi gwybodaeth fwy manwl. Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    ),
    "after_5_years_23_4": dict_for_key(
        "Please note: the following information does not contain any data for first degrees (such as BA, BSc, or Integrated Masters). Instead it is displaying information for other undergraduate qualifications – this includes CertHE, DipHE and FD among others.",
        "Sylwch: nid yw'r wybodaeth ganlynol yn cynnwys unrhyw ddata ar gyfer graddau cyntaf (fel BA, BSc neu Gwrs Meistr Integredig). Yn lle hynny, mae'n dangos gwybodaeth ar gyfer cymwysterau israddedig eraill - mae hyn yn cynnwys Tystysgrif Addysg Uwch, Diploma Addysg Uwch a Gradd Sylfaen ymhlith eraill."
    ),
    "earnings_15_months_unavailable_22_21_3": dict_for_key(
        "This includes data from this and related courses at the same university or college. There was not enough data to publish more specific information. This does not reflect on the quality of the course.",
        "Mae hwn yn cynnwys data o'r cwrs hwn a chyrsiau cysylltiedig yn yr un brifysgol neu goleg. Nid oedd digon o ddata ar gael i gyhoeddi gwybodaeth fwy manwl. Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    ),
    "earnings_15_months_unavailable_22_21_4": dict_for_key(
        "<p>This includes data from this and related courses at the same university or college. There was not enough data to publish more specific information. This does not reflect on the quality of the course.</p><p>Please note: the following information does not contain any data for first degrees (such as BA, BSc, or Integrated Masters). Instead it is displaying information for other undergraduate qualifications – this includes CertHE, DipHE and FD among others.</p>",
        "<p>Mae hwn yn cynnwys data o'r cwrs hwn a chyrsiau cysylltiedig yn yr un brifysgol neu goleg. Nid oedd digon o ddata ar gael i gyhoeddi gwybodaeth fwy manwl. Nid yw hyn yn adlewyrchu ansawdd y cwrs.</p><p>Sylwch: nid yw'r wybodaeth ganlynol yn cynnwys unrhyw ddata ar gyfer graddau cyntaf (fel BA, BSc neu Gwrs Meistr Integredig). Yn lle hynny, mae'n dangos gwybodaeth ar gyfer cymwysterau israddedig eraill - mae hyn yn cynnwys Tystysgrif Addysg Uwch, Diploma Addysg Uwch a Gradd Sylfaen ymhlith eraill.</p>"
    ),
    "unavailable_0_any": dict_for_key(
        "This is either because the course size is small or there were not enough responses to produce data. This does not reflect on the quality of the course.",
        "Mae hyn naill ai oherwydd bod y cwrs yn fach neu am nad oedd digon o ymatebion ar gael i gynhyrchu data. Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    ),
    "unavailable_1_any": dict_for_key(
        "This is because the course has not yet run or has not been running long enough for this data to be available.",
        "Mae hyn oherwydd nad yw'r cwrs wedi'i gynnal eto neu nad yw wedi cael ei gynnal yn ddigon hir i’r data hyn fod ar gael."
    ),
    "unavailable_2_any": dict_for_key(
        "This does not reflect on the quality of the course.",
        "Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    ),
    "after_3_years_23_4": dict_for_key(
        "Please note: the following information does not contain any data for first degrees (such as BA, BSc, or Integrated Masters). Instead it is displaying information for other undergraduate qualifications – this includes CertHE, DipHE and FD among others.",
        "Sylwch: nid yw'r wybodaeth ganlynol yn cynnwys unrhyw ddata ar gyfer graddau cyntaf (fel BA, BSc neu Gwrs Meistr Integredig). Yn lle hynny, mae'n dangos gwybodaeth ar gyfer cymwysterau israddedig eraill - mae hyn yn cynnwys Tystysgrif Addysg Uwch, Diploma Addysg Uwch a Gradd Sylfaen ymhlith eraill.",
    ),
    "after_3_years_21_22_3": dict_for_key(
        "his includes data from this and related courses at the same university or college. There was not enough data to publish more specific information. This does not reflect on the quality of the course.",
        "Mae hwn yn cynnwys data o'r cwrs hwn a chyrsiau cysylltiedig yn yr un brifysgol neu goleg. Nid oedd digon o ddata ar gael i gyhoeddi gwybodaeth fwy manwl. Nid yw hyn yn adlewyrchu ansawdd y cwrs.",
    ),
    "after_3_years_21_22_4": dict_for_key(
        "<p>This includes data from this and related courses at the same university or college. There was not enough data to publish more specific information. This does not reflect on the quality of the course.</p><p>Please note: the following information does not contain any data for first degrees (such as BA, BSc, or Integrated Masters). Instead it is displaying information for other undergraduate qualifications – this includes CertHE, DipHE and FD among others.</p>",
        "<p>Mae hwn yn cynnwys data o'r cwrs hwn a chyrsiau cysylltiedig yn yr un brifysgol neu goleg. Nid oedd digon o ddata ar gael i gyhoeddi gwybodaeth fwy manwl. Nid yw hyn yn adlewyrchu ansawdd y cwrs.</p><p>Sylwch: nid yw'r wybodaeth ganlynol yn cynnwys unrhyw ddata ar gyfer graddau cyntaf (fel BA, BSc neu Gwrs Meistr Integredig). Yn lle hynny, mae'n dangos gwybodaeth ar gyfer cymwysterau israddedig eraill - mae hyn yn cynnwys Tystysgrif Addysg Uwch, Diploma Addysg Uwch a Gradd Sylfaen ymhlith eraill.</p>"
    ),
    "unavailable_northern_ireland": dict_for_key(
        "Sorry, this data is not available for courses in Northern Ireland.",
        "Yn anffodus, nid yw'r data hyn ar gael ar gyfer cyrsiau yng Ngogledd Iwerddon."
    ),
    'message_1_header': {
        'en': "This and other courses",
        'cy': "Hwn a chyrsiau eraill"
    },
    'message_2_header': {
        'en': "This course over 2 years",
        'cy': "Y cwrs hwn dros 2 flynedd"
    },
    'message_3_header': {
        'en': "This and other courses over 2 years",
        'cy': "Cwrs hwn a chyrsiau eraill dros 2 flynedd"
    },
    'message_4_header': {
        'en': "This and other courses",
        'cy': "Hwn a chyrsiau eraill"
    },
    'message_5_header': {
        'en': "This course over 2 years",
        'cy': "Y cwrs hwn dros 2 flynedd"
    },
    'message_6_header': {
        'en': "This and other courses over 2 years",
        'cy': "Cwrs hwn a chyrsiau eraill dros 2 flynedd"
    },
    'message_7_header': {
        'en': "No data available",
        'cy': "Nid yw'r data ar gael"
    },
    'message_8_header': {
        'en': "This and other courses",
        'cy': "Hwn a chyrsiau eraill"
    },
    'message_9_header': {
        'en': "This and other courses over 2 years",
        'cy': "Cwrs hwn a chyrsiau eraill dros 2 flynedd"
    },
    'message_10_header': {
        'en': "No data available",
        'cy': "Nid yw'r data ar gael"
    },
    'message_11_header': {
        'en': "No data available",
        'cy': "Nid yw'r data ar gael"
    },
    'message_1': {
        'en': "The data displayed is from students on this and other courses in <b>{}</b>. " \
              "There was not enough data to publish information specifically for this course. " \
              "This may be because the course size is too small. This does not reflect on the quality of the course.",
        'cy': "Daw'r data a ddangosir gan fyfyrwyr ar y cwrs hwn a chyrsiau <b>{}</b> eraill. " \
              "Nid oedd digon o ddata i gyhoeddi gwybodaeth yn benodol ar gyfer y cwrs hwn. " \
              "Gall hyn fod oherwydd bod maint y cwrs yn rhy fach. Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    },
    'message_2': {
        'en': "This may be because the course size is too small. This does not reflect on the quality of the course.",
        'cy': "Gall hyn fod oherwydd bod maint y cwrs yn rhy fach. Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    },
    'message_3': {
        'en': "The data displayed is from students on this and other courses over two years in <b>{}</b>. " \
              "There was not enough data to publish information specifically for this course. " \
              "This may be because the course size is too small. This does not reflect on the quality of the course.",
        'cy': "Daw'r data a ddangosir gan fyfyrwyr ar y cwrs hwn a chyrsiau <b>{}</b> eraill yn ystod y ddwy flynedd flaenorol. " \
              "Nid oedd digon o ddata i gyhoeddi gwybodaeth yn benodol ar gyfer y cwrs hwn. Gall hyn fod oherwydd bod maint y cwrs yn rhy fach. " \
              "Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    },
    'message_4': {
        'en': "The data displayed is from students on this and other courses in <b>{}</b>. " \
              "There was not enough data to publish information specifically for this course. " \
              "This may be because the course size is too small or not enough students responded to the survey. " \
              "This does not reflect on the quality of the course.",
        'cy': "Daw'r data a ddangosir gan fyfyrwyr ar y cwrs hwn a chyrsiau <b>{}</b> eraill. " \
              "Nid oedd digon o ddata i gyhoeddi gwybodaeth yn benodol ar gyfer y cwrs hwn. " \
              "Gall hyn fod oherwydd bod maint y cwrs yn rhy fach neu nad oedd digon o fyfyrwyr wedi ymateb i'r arolwg. " \
              "Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    },
    'message_5': {
        'en': "This may be because the course size is too small or not enough students responded to the survey. This does not reflect on the quality of the course.",
        'cy': "Gall hyn fod oherwydd bod maint y cwrs yn rhy fach neu nad oedd digon o fyfyrwyr wedi ymateb i'r arolwg. Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    },
    'message_6': {
        'en': "The data displayed is from students on this and other courses over two years in <b>{}</b>. " \
              "There was not enough data to publish information specifically for this course. " \
              "This may be because the course size is too small or not enough students responded to the survey. This does not reflect on the quality of the course.",
        'cy': "Daw'r data a ddangosir gan fyfyrwyr ar y cwrs hwn a chyrsiau <b>{}</b> eraill yn ystod y ddwy flynedd flaenorol. " \
              "Nid oedd digon o ddata i gyhoeddi gwybodaeth yn benodol ar gyfer y cwrs hwn. " \
              "Gall hyn fod oherwydd bod maint y cwrs yn rhy fach neu nad oedd digon o fyfyrwyr wedi ymateb i'r arolwg. Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    },
    'message_7': {
        'en': "This may be because the course size is too small. This does not reflect on the quality of the course.",
        'cy': "Gall hyn fod oherwydd bod maint y cwrs yn rhy fach. Nid yw hyn yn adlewyrchu ansawdd y cwrs.",
    },
    'message_8': {
        'en': "The data displayed is from students on this and other courses in <b>{}</b>. " \
              "There was not enough data to publish information specifically for this course. " \
              "This is because the course has not yet run or has not been running long enough for this data to be available.",
        'cy': "Daw'r data a ddangosir gan fyfyrwyr ar y cwrs hwn a chyrsiau <b>{}</b> eraill. " \
              "Nid oedd digon o ddata i gyhoeddi gwybodaeth yn benodol ar gyfer y cwrs hwn. " \
              "Mae hyn oherwydd nad yw'r cwrs wedi'i gynnal eto neu nid yw wedi cael ei gynnal yn ddigon hir i’r data hwn fod ar gael."
    },
    'message_9': {
        'en': "The data displayed is from students on this and other courses over two years in <b>{}</b>. " \
              "There was not enough data to publish information specifically for this course. " \
              "This is because the course has not yet run or has not been running long enough for this data to be available.",
        'cy': "Daw'r data a ddangosir gan fyfyrwyr ar y cwrs hwn a chyrsiau <b>{}</b> eraill yn ystod y ddwy flynedd flaenorol. " \
              "Nid oedd digon o ddata i gyhoeddi gwybodaeth yn benodol ar gyfer y cwrs hwn. " \
              "Mae hyn oherwydd nad yw'r cwrs wedi'i gynnal eto neu nid yw wedi cael ei gynnal yn ddigon hir i’r data hwn fod ar gael."
    },
    'message_10': {
        'en': "This is because the course has not yet run or has not been running long enough for this data to be available. This does not reflect on the quality of the course.",
        'cy': "Mae hyn oherwydd nad yw'r cwrs wedi'i gynnal eto neu nid yw wedi cael ei gynnal yn ddigon hir i’r data hwn fod ar gael. Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    },
    'message_11': {
        'en': "This does not reflect on the quality of the course.",
        'cy': "Nid yw hyn yn adlewyrchu ansawdd y cwrs."
    },
    "this_course": {
        'en': "This course",
        'cy': "Y cwrs hwn"
    },
    "data_displayed": {
        'en': "The data displayed is from students on",
        'cy': "Daw’r data a ddangosir gan fyfyrwyr ar y cwrs"
    }
}
