from faculty_calender import FacultyCalender
from faculty_calender_resources.faculty_of_arts_and_science_calender import FacultyOfArtsAndScienceCalender
from faculty_calender_resources.session import Session
from faculty_calender_resources.session import Season
from faculty_calender_resources.url import URL

cal = FacultyOfArtsAndScienceCalender(Session(2016, Season.FALL),
                                      URL("http://calendar.artsci.utoronto.ca"))
deps = cal.get_department_calenders()

courses = []
for dep in deps:
    courses.extend(dep.get_courses())

file = open("courses.txt", 'w')
delimiter = '\n' * 5
file.write(delimiter.join(sorted([str(course) for course in courses])))
