import re

from bs4 import BeautifulSoup

from raw_html import get_html
from department_calender import DepartmentCalender


class FacultyCalender:
    """
    Represents an instance of a faculty calender for a particular year.

    This class currently only supports the faculty calenders from 2011-2012
    onwards
    """

    # the current year faculty calender url
    url = "http://calendar.artsci.utoronto.ca"

    # the raw html for the current year faculty calender
    raw_html = get_html(url)

    # the BeautifulSoup object used to parse the current year faculty calender
    soup = BeautifulSoup(raw_html, "html5lib")

    def __init__(self, year, url):
        """
        Initialize a new Faculty Calender for the given url

        :param url: The url to the specified year's calender
        :type url: str
        :return: A FacultyCalender object for the given url
        :rtype: FacultyCalender
        """
        self.year = year
        self.url = url
        self.raw_html = get_html(self.url)
        self.soup = BeautifulSoup(self.raw_html, 'html5lib')
        self.department_calenders = []

    def get_department_calenders(self):
        raise NotImplementedError

    @staticmethod
    def get_faculty_calenders():
        """ Retrieve a dictionary of all the links to previous years calenders.

        Note: not all of the calenders are available on the U of T website

        Note: the older calenders do not follow the same style as the more
              current ones so they may not be supported

        :return: all of the found FacultyCalender
        :rtype: dict{str : FacultyCalender}
        """

        # the title contains the string 20XX-20XX indicating the current year
        # from the 0th to 8th characters inclusive
        current_year = FacultyCalender.soup.title.string[:9]

        # a dictionary mapping the year to the url to that year's calender
        # the takes the form XXXX-YYYY where XXXX is the starting year and
        # YYYY is the ending year (eg. 2016-2017)
        calenders = dict()

        calenders[current_year] = FacultyCalender2011To2012Onwards\
            (current_year, FacultyCalender.url)

        for a_tag in FacultyCalender.soup.find_all('a'):
            url = a_tag['href']
            if FacultyCalender._match_archived_calender_url(url):
                year = str(a_tag.string).strip()
                full_url = FacultyCalender.url + '/' + url

                # TODO: add support for years before 2011-2012
                # add the calender to the dictionary if it is one of the
                # calenders from the supported years
                if FacultyCalender._is_supported(year):
                    calenders[year] = FacultyCalender2011To2012Onwards(year,
                                                                       full_url)
        return calenders

    @staticmethod
    def _is_supported(year):
        """ Return True if the year is supported by this Faculty Calender class

        :param year: the year of the calender
        :type year: str
        :return: True if the calender is supported
        :rtype: bool
        """
        year = [int(time) for time in year.split('-')]
        return year[0] >= 2011 and year[1] >= 2012

    _archived_calender_url = \
        re.compile("archived/\\d\\d\\d\\dcalendar/index\.html")

    @staticmethod
    def _match_archived_calender_url(url):
        """ Return True if the url matches what is expected of an archived
        calender url

        :param url: a possible archived calender url
        :type url: str
        :return: True if it matches an archived calender url
        :rtype: bool
        """
        return FacultyCalender._archived_calender_url.match(url) is not None

    def _to_full_url(self, url):
        """Converts a partial url to the full url by appending it to the main
        part of the url

        :param url: the partial url
        :type url: str
        :return: the full url
        :rtype: str
        """
        if self.url == FacultyCalender.url:
            return self.url + "/" + url
        else:
            # the last 11 characters contains index.html which is to be cut off
            return self.url[:-11] + "/" + url


class FacultyCalender2011To2012Onwards(FacultyCalender):

    def get_department_calenders(self):
        """
        Gets the Department Calenders found on this Faculty Calender

        :return: a list of Department Calenders found
        :rtype: list[DepartmentCalender]
        """

        for a_tag in self.soup.find_all('a'):
            url = a_tag['href']
            if FacultyCalender2011To2012Onwards.\
                    _match_department_calender_url(url):
                department = str(a_tag.string).strip()
                full_url = self._to_full_url(url)

                # add a new Department Calender instance to the list
                calender = DepartmentCalender(department, self.year, full_url)
                self.department_calenders.append(calender)

        return self.department_calenders.copy()

    _department_calender_url = re.compile("crs_\\w\\w\\w.htm")

    @staticmethod
    def _match_department_calender_url(url):
        """ Return True if the url matches what is expected of a department
        calender url

        :param url: a possible department calender url
        :type url:  str
        :return: True if it matches a department calender url
        :rtype: bool
        """
        return FacultyCalender2011To2012Onwards.\
            _department_calender_url.match(url) is not None

def filter_for_breadth_2_and_4(courses):
    filtered = []
    for course in courses:
        if int(course.course_code[3]) <= 2:
            if course.breadth_requirement == 'Thought, Belief and Behaviour (2)' or course.breadth_requirement == 'Living Things and Their Environment (4)':
                filtered.append(str(course))
    return filtered


if __name__ == '__main__':
    faculty_calenders = FacultyCalender.get_faculty_calenders()
    all_courses = []
    faculty_calender = faculty_calenders['2016-2017']
    department_calenders = faculty_calender.get_department_calenders()
    for department_calender in department_calenders:
        all_courses.extend([course for course in department_calender.get_courses()])

    open('breadth.txt', 'w').write('\n--------------------\n'.join(filter_for_breadth_2_and_4(all_courses)))
