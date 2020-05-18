
class FilterForm:

    def __init__(self, form_data):
        self.countries_query = ','.join(form_data.getlist('countries_query')) if 'countries_query' in form_data \
            else ''
        self.mode_query = ','.join(form_data.getlist('mode_query')) if 'mode_query' in form_data else ''
        self.qualification_query = form_data.get('qualification_query')
        self.placement = form_data.get('placement')
        self.foundation = form_data.get('foundation')
        self.abroad = form_data.get('abroad')
        self.institutions = form_data.get('institution_query', '').replace('"', '')
        self.courses = form_data.get('subject_query', '')
        self.course_query = form_data.get('course_query', '')
        postcode_query = form_data.get('postcode_query')
        if postcode_query:
            self.postcode = postcode_query.split(',')[0]
            self.distance = postcode_query.split(',')[1]
        else:
            self.postcode = ''
            self.distance = ''
