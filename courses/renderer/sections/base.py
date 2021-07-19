from typing import List, Dict, Any, Tuple

from CMS import translations
from courses.models import Course


def empty_data_structure(key: str, language: str) -> Dict[str, Any]:
    return dict(title=translations.term_for_key(key=key, language=language), values=[])


primary_key = 0
action = 1


class Section:

    def __init__(self, courses: List[Course], language: str):
        self.data = {}
        self.courses = courses
        self.language = language
        super().__init__()

    def get_sections(self) -> List[Tuple[Any, Any]]:
        raise NotImplementedError

    def prep_data(self):
        self.data = {}
        for section in self.get_sections():
            self.data[section[primary_key]] = empty_data_structure(section[primary_key], self.language)

    def generate_dict(self) -> dict:
        raise NotImplementedError
