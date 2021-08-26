from courses.renderer.sections.base import Section

class InformationSection(Section):
    def prep_data(self):
        self.data = {}
        self.data['info'] = self.empty_data_structure('Link to website', self.language)

    def generate_dict(self) -> dict:
        for course in self.courses:
            self.data['info']['values'].append(course.institution_name)
            # for link in course.course_links:
            #
            #     self.data['info']['values'].append(link)
        return self.data
