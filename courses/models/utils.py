from CMS.enums import enums


def display_unavailable_info(self, aggregation_level, subject_welsh, replace=False):
    unavailable = {}

    if self.unavailable_reason:
        unavailable["reason"] = self.unavailable_reason
    else:
        if self.display_language == enums.languages.ENGLISH:
            unavailable["reason"] = self.unavailable_reason_english if self.unavailable_reason_english \
                else self.unavailable_reason_welsh
        else:
            unavailable[
                "reason"] = self.unavailable_reason_welsh if self.unavailable_reason_welsh else self.unavailable_reason_english

    if self.display_language == enums.languages.ENGLISH:
        unavailable[
            "find_out_more"] = self.unavailable_find_out_more_english if self.unavailable_find_out_more_english \
            else self.unavailable_find_out_more_welsh
    else:
        unavailable[
            "find_out_more"] = self.unavailable_find_out_more_welsh if self.unavailable_find_out_more_welsh else self.unavailable_find_out_more_english

    if "reason" in unavailable:
        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(
                                                                        unavailable["reason"],
                                                                        subject_welsh
                                                                    )


        #TODO: Remove once OFS want the override disabled https://app.clickup.com/t/j337mq
        if replace and str(aggregation_level) in ["21", "22", "23"]:

            if self.display_language == enums.languages.ENGLISH:
                unavailable["reason_heading"] = unavailable["reason_heading"].replace(" over the previous two years", "")
            else:
                unavailable["reason_heading"] = unavailable["reason_heading"].replace("eraill yn ystod y ddwy flynedd flaenorol",
                                                                           "eraill")

        elif replace and str(aggregation_level) == "24":
            unavailable["reason_body"] = None
        # end remove


    return unavailable


def separate_unavail_reason(reason_unseparated, subject_welsh=""):
    subject_welsh = subject_welsh if subject_welsh is not None else ""
    WELSH_UNAVAILABLE_UPDATES = [
        ["yn ystod y ddwy flynedd flaenorol", "dros dwy flynedd"],
        ["Daw'r data a ddangosir gan fyfyrwyr ar y cwrs hwn a chyrsiau Gemau cyfrifiadurol ac animeiddio eraill",
         f"Daw'r data a ddangosir gan fyfyrwyr ar y cwrs hwn a chyrsiau eraill mewn {subject_welsh}"],
        ["Nid yw hyn yn adlewyrchu ansawdd y cwrs.", "Nid yw hyn yn adlewyrchu ar ansawdd y cwrs."],
        [f"Daw'r data a ddangosir gan fyfyrwyr ar y cwrs hwn a chyrsiau Eraill mewn {subject_welsh} eraill yn ystod y ddwy flynedd flaenorol.",
         f"Daw'r data a ddangosir gan fyfyrwyr ar y cwrs hwn a chyrsiau eraill dros dwy flynedd {subject_welsh}."]
    ]
    index_of_delimiter = reason_unseparated.find('\n\n')

    if index_of_delimiter > 4:
        reason_heading = reason_unseparated[:index_of_delimiter]
        for replacement in WELSH_UNAVAILABLE_UPDATES:
            reason_heading = reason_heading.replace(replacement[0], replacement[1])
        reason_body = reason_unseparated[index_of_delimiter + 2:]
    else:
        reason_heading = reason_unseparated
        reason_body = ""

    return reason_heading, reason_body


def display_subject_name(self):
    if self.display_language == enums.languages.ENGLISH:
        return self.subject_english if self.subject_english else self.subject_welsh
    return self.subject_welsh if self.subject_welsh else self.subject_english
