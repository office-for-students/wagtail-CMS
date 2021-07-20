from .utils import fallback_to


class CourseCodeGeneric:
    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = fallback_to(data_obj.get('label'), '')


class CourseMode(CourseCodeGeneric):
    pass


class CourseQualification(CourseCodeGeneric):
    pass


class CourseSandwichYear(CourseCodeGeneric):
    pass


class CourseYearAbroad(CourseCodeGeneric):
    pass


class CourseCountry(CourseCodeGeneric):
    pass
