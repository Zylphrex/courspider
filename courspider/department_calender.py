import re

from bs4 import BeautifulSoup

from raw_html import get_html
from course import Course


class DepartmentCalender:

    _match = re.compile('<!--\[if.*?\]>.*?<!\[endif\]-->', re.DOTALL)

    def __init__(self, department, year, url):
        self.department = department
        self.year = year
        self.url = url
        self.soup = BeautifulSoup(get_html(url), 'html5lib')

        # remove \xa0 and replace with spaces
        self.raw_html = str(self.soup).replace(u'\xa0', u' ')
        for match in DepartmentCalender._match.findall(self.raw_html):
            self.raw_html = self.raw_html.replace(match, '')

    # regular expression used to filter out the course data
    _course = re.compile('<a name="([A-Z]{3}\\d\\d\\d[A-Z]\\d)"></a><span '
                         'class="strong">\\1    (.*?)<\/span><p(.*?)?>(.*?)</p>'
                         '.*?(Exclusion:\s*(.*?)|Prerequisite:\s*(.*?)|'
                         'Corequisite:\s*(.*?))?(<br/>)?'
                         '.*?(Exclusion:\s*(.*?)|Prerequisite:\s*(.*?)|'
                         'Corequisite:\s*(.*?))?(<br/>)?'
                         '.*?(Exclusion:\s*(.*?)|Prerequisite:\s*(.*?)|'
                         'Corequisite:\s*(.*?))?(<br/>)?'
                         'Distribution Requirement Status:\s*(.*?)<br/>'
                         'Breadth Requirement:\s*(.*?)<br/>', re.DOTALL)

    def get_courses(self):
        courses = []
        courses_data = DepartmentCalender._course.findall(self.raw_html)

        for course_data in courses_data:
            courses.append(DepartmentCalender._create_course(course_data))

        return courses

    @staticmethod
    def _create_course(data):
        # these numbers come from the group numbers from the regex above
        # '_course' count them if you wanna
        course_code = DepartmentCalender._erase_html(data[0])
        course_name = DepartmentCalender._erase_html(data[1])
        course_description = DepartmentCalender._erase_html(data[3])
        exclusion = DepartmentCalender._erase_html(
            data[5] + data[10] + data[15])
        prerequisite = DepartmentCalender._erase_html(
            data[6] + data[11] + data[16])
        corequisite = DepartmentCalender._erase_html(
            data[7] + data[12] + data[17])
        distribution_requirement = DepartmentCalender._erase_html(
            data[19])
        breath_requirement = DepartmentCalender._erase_html(data[20])

        return Course(course_code, course_name, course_description,
                      exclusion, prerequisite, corequisite,
                      distribution_requirement, breath_requirement)

    _link = re.compile('<a href=".*?">(.*?)</a>')
    _break = re.compile('<br/>')
    _para_start = re.compile('<p>')
    _para_end = re.compile('</p>')

    @staticmethod
    def _erase_html(data):
        data = DepartmentCalender._link.sub("\\1", data)
        data = DepartmentCalender._break.sub('', data)
        data = DepartmentCalender._para_start.sub('', data)
        data = DepartmentCalender._para_end.sub('', data)
        return data

