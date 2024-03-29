from CMS import translations
from courses.renderer.sections.base import Section


class InformationSection(Section):
    def prep_data(self):
        self.data = {}
        self.data['info'] = self.empty_data_structure('Link to website', self.language)

    def generate_dict(self) -> dict:
        alt_text = translations.term_for_key(key="open_tab", language=self.language)
        for course in self.courses:
            link = course.course_links['course_details'][0].link
            self.data['info']['values'].append(
                f"<a class='institution-link' href='{link}' target='_blank'>{course.institution_name}"
                f"<img src='/static/images/new_tab_icon.png' alt={alt_text}></a>")
        return self.data
