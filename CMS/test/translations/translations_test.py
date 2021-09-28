from new import term_for_key
from old import DICT, STATISTICS, OPTIONALS, UNAVAILABLE

dicts = dict(DICT, **STATISTICS, **OPTIONALS, **UNAVAILABLE)
english_pass_count = 0
english_fails = []
welsh_pass_count = 0
welsh_fails = []

for key, value in dicts.items():
    try:
        assert term_for_key(key, 'en') == value.get('en'), f"English Failed for value {value}"
        english_pass_count += 1
    except Exception:
        english_fails.append(key)
    try:
        assert term_for_key(key, 'cy') == value.get('cy'), f"Welsh Failed for value {value}"
        welsh_pass_count += 1
    except Exception:
        welsh_fails.append(key)

print(english_pass_count, 'English tests passed')
print(welsh_pass_count, 'Welsh tests passed')
print(english_fails)
print(welsh_fails)

