from CMS.enums import enums
from core.request_handler import get_json_file


def not_already_in_list(name, existing):
    if name not in existing:
        existing.append(name)
        return True
    return False


def load_institution_json():
    institution_json = {}

    for language, _language_full in enums.languages_map.items():
        response = get_json_file("institutions_" + language + ".json")
        data = response.json()
        de_duped = []
        final = [name for name in data if not_already_in_list(name=name["name"], existing=de_duped)]

        response_body = final if response.ok else {}

        institution_json[language] = response_body
        
    return institution_json
