import re

from bs4 import BeautifulSoup

from faculty_calender import FacultyCalender
from faculty_calender_resources.department import Department
from faculty_calender_resources.faculty import Faculty
from faculty_calender_resources.url import URL
from department_calender import DepartmentCalender


class FacultyOfArtsAndScienceCalender(FacultyCalender):

    def __init__(self, session, url):
        """
        Represents the calender of the Faculty of Arts and Science

        :param session: The session of the calender
        :type session: Session
        :param url: The url to the specified year's calender
        :type url: URL
        :return: A FacultyCalender object for the given url
        :rtype: FacultyCalender
        """
        super().__init__(Faculty.ARTS_AND_SCIENCE, session, url)
        self.soup = BeautifulSoup(url.raw_html, "html5lib")

    def _generate_department_calenders_from_html(self):
        """
        Using the unescaped raw html of the calender, create and return all the
        department calenders found.

        :return: list of Department Calender objects generated from this Faculty
                 Calender
        :rtype: list[DepartmentCalender]
        """

        dpeartment_calenders = []
        department_urls = []

        # generates a list of all the url endings found
        print("finding all url endings to department calenders")
        for a_tag in self.soup.find_all('a'):
            url = a_tag['href']

            if FacultyOfArtsAndScienceCalender.\
                    _match_department_calender_url(url):
                print("found url endings to department calender at {}".format(url))
                department_urls.append(url)

        print("removing duplicate department url")
        # eliminate duplicate urls
        department_urls = set(department_urls)

        # generates a list of department calenders from the list of url endings
        for department_url in department_urls:
            print("converting {} to full url".format(department_url))
            url = self._to_full_url(department_url)
            calender = DepartmentCalender(self.session, url)
            self.department_calenders.append(calender)

        return self.department_calenders

    def _to_full_url(self, url):
        """
        Return the full url for the link by concatenating the url ending to the
        Faculty Calender url

        :parm url: The ending the the Department Calender url
        :type url: str
        :return: The url to the Department Calender
        :rtype: URL
        """
        return URL(self.url.url + '/' + url)

    # regex used for the _match_department_calender_url method
    _department_calender_url = re.compile(r"crs_\w\w\w.htm")

    @staticmethod
    def _match_department_calender_url(url):
        """ Return True if the url matches what is expected of a department
        calender url

        :param url: a possible department calender url
        :type url:  str
        :return: True if it matches a department calender url
        :rtype: bool
        """
        return FacultyOfArtsAndScienceCalender.\
            _department_calender_url.fullmatch(url) is not None
