class Course:

    labels = ['Course code', 'Course name', 'Course description',
             'Course exclusion', 'Course prerequisite',
             'Course corequisite', 'Course preparation',
             'Course distribution requirement',
             'Course breadth requirement']

    def __init__(self, course_code, course_name, course_description,
                 exclusion, prerequisite, corequisite, recommended,
                 distribution_requirement, breadth_requirement):
        self.course_code = Course._set(course_code)
        self.course_name = Course._set(course_name)
        self.course_description = Course._set(course_description)
        self.exclusion = Course._set(exclusion)
        self.prerequisite = Course._set(prerequisite)
        self.corequisite = Course._set(corequisite)
        self.recommended = Course._set(recommended)
        self.distribution_requirement = Course._set(distribution_requirement)
        self.breadth_requirement = Course._set(breadth_requirement)

        self.data = [self.course_code, self.course_name,
                     self.course_description, self.exclusion,
                     self.prerequisite, self.corequisite, self.recommended,
                     self.distribution_requirement, self.breadth_requirement]

    def __str__(self):
        delimiter = '\n' + ('-' * 80) + '\n'
        return delimiter.join([label + ': ' + data for label, data in \
                zip(Course.labels, self.data)])

    @staticmethod
    def _set(val):
        val = val.strip()
        return val if val is not "" else 'None'
