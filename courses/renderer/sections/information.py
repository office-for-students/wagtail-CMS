from courses.renderer.sections.base import Section


class InformationSection(Section):
    def prep_data(self):
        self.data = {}
        self.data['info'] = self.empty_data_structure('Link to website', self.language)

    def generate_dict(self) -> dict:
        for course in self.courses:
            link = course.course_links['course_details'][0].link
            self.data['info']['values'].append(
                f"<a class='institution-link' href='{link}' target='_blank'>{course.institution_name}</a>")
        return self.data
