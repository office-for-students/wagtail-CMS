
class FilterForm:

    def __init__(self, form_data):
        self.countries_query = form_data.get('countries_query')
        self.mode_query = form_data.get('mode_query')
        self.placement = form_data.get('placement')
        self.foundation = form_data.get('foundation')
        self.abroad = form_data.get('abroad')
        self.institutions = form_data.get('institution_query', '')
        self.courses = form_data.get('subject_query', '')
        postcode_query = form_data.get('postcode_query')
        if postcode_query:
            self.postcode = postcode_query.split(',')[0]
            self.distance = postcode_query.split(',')[1]
