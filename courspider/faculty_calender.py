import re

from bs4 import BeautifulSoup

from raw_html import get_html
from department_calender import DepartmentCalender


class FacultyCalender:

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

    def get_department_calenders(self):
        """
        Gets the Department Calenders found on this Faculty Calender

        :return: a list of Department Calenders found
        :rtype: list[DepartmentCalender]
        """
        calenders = []

        for a_tag in self.soup.find_all('a'):
            url = a_tag['href']
            if FacultyCalender._match_department_calender_url(url):
                department = str(a_tag.string).strip()
                full_url = FacultyCalender._to_full_url(url)

                # add a new Department Calender instance to the list
                calenders.append(DepartmentCalender(department, self.year,
                                                    full_url))

        return calenders

    @staticmethod
    def _match_department_calender_url(url):
        """ Return True if the url matches what is expected of a department
        calender url

        :param url: a possible department calender url
        :type url:  str
        :return: True if it matches a department calender url
        :rtype: bool
        """
        regex = "crs_\\w\\w\\w.htm"
        return re.match(regex, url) is not None

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

        calenders[current_year] = FacultyCalender(current_year,
                                                  FacultyCalender.url)

        for a_tag in FacultyCalender.soup.find_all('a'):
            url = a_tag['href']
            if FacultyCalender._match_archived_calender_url(url):
                year = str(a_tag.string).strip()
                full_url = FacultyCalender._to_full_url(url)

                # add the calender to the dictionary if it is one of the
                # calenders from the supported years
                if FacultyCalender._is_supported(year):
                    calenders[year] = FacultyCalender(year, full_url)

        return calenders

    @staticmethod
    def _match_archived_calender_url(url):
        """ Return True if the url matches what is expected of an archived
        calender url

        :param url: a possible archived calender url
        :type url: str
        :return: True if it matches an archived calender url
        :rtype: bool
        """
        regex = "archived/\\d\\d\\d\\dcalendar/index\.html"
        return re.match(regex, url) is not None

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

    @staticmethod
    def _to_full_url(url):
        """Converts a partial url to the full url by appending it to the main
        part of the url

        :param url: the partial url
        :type url: str
        :return: the full url
        :rtype: str
        """
        return FacultyCalender.url + "/" + url
