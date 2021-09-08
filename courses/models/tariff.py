from typing import List

from .utils import enums, fallback_to

LABELS_ENGLISH = {
    "T001": "Less than 48",
    "T048": "48 - 63",
    "T064": "64 - 79",
    "T080": "80 - 95",
    "T096": "96 - 111",
    "T112": "112 - 127",
    "T128": "128 - 143",
    "T144": "144 - 159",
    "T160": "160 - 175",
    "T176": "176 - 191",
    "T192": "192 - 207",
    "T208": "208 - 223",
    "T224": "224 - 239",
    "T240": "More than 240",
}

LABELS_WELSH = {
    "T001": "Llai na 48",
    "T048": "48 - 63",
    "T064": "64 - 79",
    "T080": "80 - 95",
    "T096": "96 - 111",
    "T112": "112 - 127",
    "T128": "128 - 143",
    "T144": "144 - 159",
    "T160": "160 - 175",
    "T176": "176 - 191",
    "T192": "192 - 207",
    "T208": "208 - 223",
    "T224": "224 - 239",
    "T240": "Mwy na 240",
}


class Tariff:

    def __init__(self, tariff, language):
        self.code = tariff.get('code')
        self.description = fallback_to(tariff.get('description'), '')
        self.entrants = fallback_to(tariff.get('entrants'), 0)
        self.display_language = language

    @property
    def label(self):
        if self.code:
            if self.display_language == enums.languages.ENGLISH:
                return LABELS_ENGLISH[self.code]
            else:
                return LABELS_WELSH[self.code]
        return ''


def tariff_range(tariff_list: List, language: str) -> str:
    min_code = tariff_list[0]["code"]
    max_code = tariff_list[-1]["code"]

    if language == enums.languages.ENGLISH:
        first = LABELS_ENGLISH[min_code]
        last = LABELS_ENGLISH[max_code]
    else:
        first = LABELS_WELSH[min_code]
        last = LABELS_ENGLISH[max_code]

    min_split = first.split("-")
    first_range = min_split[0]
    max_split = last.split("-")
    last_range = max_split[-1]

    return first_range + " - " + last_range


