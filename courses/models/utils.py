from CMS.enums import enums as original_enums
from core.utils import fallback_to as fallback_available
import CMS.translations

enums = original_enums
fallback_to = fallback_available
DICT = CMS.translations.DICT


def separate_unavail_reason(reason_unseparated):
    index_of_delimiter = reason_unseparated.find('\n\n')

    if index_of_delimiter > 4:
        reason_heading = reason_unseparated[:index_of_delimiter]
        reason_body = reason_unseparated[index_of_delimiter + 2:]
    else:
        reason_heading = reason_unseparated
        reason_body = ""

    return reason_heading, reason_body


import json

from typing import List

import requests

from CMS.translations import DICT
from core.models import DiscoverUniBasePage

from courses import request_handler
from errors.models import ApiError
from institutions.models import InstitutionOverview


