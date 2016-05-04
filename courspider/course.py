class Course:

    def __init__(self, course_code, course_name, course_description,
                 exclusion, prerequisite, corequisite,
                 distribution_requirement, breadth_requirement,):
        self.course_code = course_code
        self.course_name = course_name
        self.course_description = course_description
        self.distribution_requirement = distribution_requirement
        self.breadth_requirement = breadth_requirement
        self.exclusion = exclusion
        self.prerequisite = prerequisite
        self.corequisite = corequisite

    def __str__(self):
        string = ""
        string += "Course code:"
        string += self.course_code
        string += '\n'
        string += "Course name:"
        string += self.course_name
        string += '\n'
        string += "Course description:"
        string += self.course_description
        string += '\n'
        string += "Course exclusion:"
        string += self.exclusion
        string += '\n'
        string += "Course prerequisite:"
        string += self.prerequisite
        string += '\n'
        string += "Course corequisite:"
        string += self.corequisite
        string += '\n'
        string += "Course distribution requirement:"
        string += self.distribution_requirement
        string += '\n'
        string += "Course breath requirement:"
        string += self.breadth_requirement
        return string
