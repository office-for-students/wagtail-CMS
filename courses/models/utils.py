import CMS.translations
from CMS.enums import enums


def display_unavailable_info(self, aggregation_level, replace=False):
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
        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        if replace and str(aggregation_level) in ["11", "12", "13", "21", "22", "23"]:
            if self.display_language == enums.languages.ENGLISH:
                unavailable["reason_body"] = unavailable["reason_body"].replace(" over the previous two years", "")
            else:
                unavailable["reason_body"] = unavailable["reason_body"].replace("eraill yn ystod y ddwy flynedd flaenorol",
                                                                           "eraill")
    return unavailable


def separate_unavail_reason(reason_unseparated):
    index_of_delimiter = reason_unseparated.find('\n\n')

    if index_of_delimiter > 4:
        reason_heading = reason_unseparated[:index_of_delimiter]
        reason_body = reason_unseparated[index_of_delimiter + 2:]
    else:
        reason_heading = reason_unseparated
        reason_body = ""

    return reason_heading, reason_body
