# Use this to access DICT/OPTIONS, don't access them directly
import re
import string

from .dictionaries import general
from .dictionaries import jobs
from .dictionaries import statistics
from .dictionaries import unavailable


def cleanup_key(key):
    exclude = set(string.punctuation) - {'_', '-'}
    new = ''.join(ch for ch in key if ch not in exclude)
    new = re.sub('\s|[-]', '_', new)

    return new.lower()


def term_for_key(key: str, language: str) -> str:
    """ Method to use to access welsh translations for static content
        returns: a language specific translation or the origin key string passed in if it can't be found.
    """
    if key is not None:
        key = cleanup_key(key)
    term = general.DICT.get(key).get(language) if key in general.DICT else None
    if not term:
        term = statistics.STATISTICS.get(key).get(language) if key in statistics.STATISTICS else None
    if not term:
        term = unavailable.UNAVAILABLE.get(key).get(language) if key in unavailable.UNAVAILABLE else None
    if not term:
        term = jobs.JOBS.get(key).get(language) if key in jobs.JOBS else None
    if not term:
        term = general.OPTIONALS.get(key).get(language) if key in general.OPTIONALS else None
    if not term:
        term = key
    return term
