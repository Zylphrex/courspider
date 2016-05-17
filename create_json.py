import json


from courspider.faculty_calendar import FacultyCalendar
from courspider.faculty_calendar_resources.faculty_of_arts_and_science_calendar import FacultyOfArtsAndScienceCalendar
from courspider.faculty_calendar_resources.session import Session
from courspider.faculty_calendar_resources.session import Season
from courspider.faculty_calendar_resources.url import URL

cal = FacultyOfArtsAndScienceCalendar(Session(2016, Season.FALL),
                                      URL("http://calendar.artsci.utoronto.ca"))

print('getting department calendars')
deps = cal.get_department_calendars()

course_datas = []

print('getting course datas')
for dep in deps:
    for course in dep.get_courses():
        course_datas.append(course.to_data())

file = open("courses/courses.json", 'w')
file.write(json.dumps({"courses":course_datas}, indent=4))
