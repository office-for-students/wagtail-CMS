import re
import string

from CMS import translations
from .job import Job
from .utils import enums, fallback_to


class JobList:

    def __init__(self, jobs_data, display_language):
        self.display_language = display_language
        self.jobs = []

        if jobs_data:
            self.aggregation = jobs_data.get('aggregation')
            self.number_of_students = fallback_to(jobs_data.get('number_of_students'), 0)
            self.response_rate = str(fallback_to(jobs_data.get('response_rate'), 0)) + '%'

            subject_data = fallback_to(jobs_data.get('subject'), {})
            self.subject_code = subject_data.get('code', '')
            self.subject_english = subject_data.get('english_label', '')
            self.subject_welsh = subject_data.get('welsh_label', '')

            unavailable_data = fallback_to(jobs_data.get('unavailable'), {})
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')
            self.unavailable_reason_english = fallback_to(unavailable_data.get('reason_english'), '')
            self.unavailable_reason_welsh = fallback_to(unavailable_data.get('reason_welsh'), '')
            self.unavailable_find_out_more_english = fallback_to(unavailable_data.get('find_out_more_english'), '')
            self.unavailable_find_out_more_welsh = fallback_to(unavailable_data.get('find_out_more_welsh'), '')
            self.unavailable_url_english = fallback_to(unavailable_data.get('url_english'), '')
            self.unavailable_url_welsh = fallback_to(unavailable_data.get('url_welsh'), '')

            if jobs_data.get('list'):
                for job in jobs_data.get('list'):
                    job['job'] = translations.term_for_key(
                        key=self.format_job_title(job['job']), language=self.display_language)
                    self.jobs.append(Job(job, self.display_language))

    @staticmethod
    def format_job_title(title):
        exclude = set(string.punctuation) - {'_', '-'}
        new = ''.join(ch for ch in title if ch not in exclude)
        new = re.sub('\s', '_', new)
        return new.lower()

    def show_stats(self):
        return self.jobs

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english

    def display_unavailable_info(self):
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

        if self.display_language == enums.languages.ENGLISH:
            unavailable["url"] = self.unavailable_url_english if self.unavailable_url_english \
                else self.unavailable_url_welsh
        else:
            unavailable[
                "url"] = self.unavailable_url_welsh if self.unavailable_url_welsh else self.unavailable_url_english

        if "reason" in unavailable:
            if self.aggregation in ["21", "22", "23"]:
                if self.display_language == enums.languages.ENGLISH:
                    unavailable["reason"] = unavailable["reason"].replace(" over the previous two years", "")
                else:
                    unavailable["reason"] = unavailable["reason"].replace("eraill yn ystod y ddwy flynedd flaenorol",
                                                                          "eraill")

        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable
