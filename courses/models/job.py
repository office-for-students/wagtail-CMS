from .utils import enums, fallback_to


class Job:

    def __init__(self, job_data, display_language):
        self.display_language = display_language
        if job_data:
            self.job = fallback_to(job_data.get('job'), '')
            self.percentage = fallback_to(job_data.get('percentage_of_students'), 0)

            if self.display_language == enums.languages.ENGLISH:
                self.percentage = self.percentage.replace('<5', 'Less than 5')
            else:
                self.percentage = self.percentage.replace('<5', 'Llai na 5')

            self.order = job_data.get('order')
            self.hs = fallback_to(job_data.get('hs'), '')
