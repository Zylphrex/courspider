import json


from courspider.faculty_calendar import FacultyCalendar
from courspider.faculty_calendar_resources.faculty_of_arts_and_science_calendar import FacultyOfArtsAndScienceCalendar
from courspider.faculty_calendar_resources.department import Department
from courspider.faculty_calendar_resources.session import Session
from courspider.faculty_calendar_resources.session import Season
from courspider.faculty_calendar_resources.url import URL

def create_course_json():
    cal = FacultyOfArtsAndScienceCalendar(Session(2016, Season.FALL),
                                          URL("http://calendar.artsci.utoronto.ca"))

    print('getting department calendars')
    deps = cal.get_department_calendars()

    course_datas = []

    print('getting course datas')
    for dep in deps:
        for course in dep.get_courses():
            course_datas.append(course.to_data())

    file = open("data/courses.json", 'w')
    file.write(json.dumps({"courses": course_datas}, indent=4))
    print('course data written')

def create_department_json():
    cal = FacultyOfArtsAndScienceCalendar(Session(2016, Season.FALL),
                                          URL("http://calendar.artsci.utoronto.ca"))
    print('getting department calendars')
    departments = [department.name for department in cal.get_departments()]

    file = open("data/departments.json", 'w')
    file.write(json.dumps({"departments": departments}, indent=4))
    print('department data written')
