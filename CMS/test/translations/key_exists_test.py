import time

from new import term_for_key
from new_jobs import jobs

counter = 0
length = len(jobs)
for job in jobs:
    term, key = term_for_key(job, 'en')
    assert term != key, f"Key {key} not present"
    print(f"Key {key} exists in dictionary")
    counter += 1
    time.sleep(0.01)

print(f"{counter} tests passed")
print(f"{length - counter} tests failed")
if length - counter == 0:
    print('All keys present')
