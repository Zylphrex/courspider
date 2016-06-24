import json


from courspider.faculty_calendar import FacultyCalendar
from courspider.faculty_calendar_resources.faculty_of_arts_and_science_calendar import FacultyOfArtsAndScienceCalendar
from courspider.faculty_calendar_resources.department import Department
from courspider.faculty_calendar_resources.session import Session
from courspider.faculty_calendar_resources.session import Season
from courspider.faculty_calendar_resources.url import URL


def write_data(data, dest):
    file = open(dest, 'w')
    file.write(json.dumps(data, indent=4))

def _create_course_data():
    cal = FacultyOfArtsAndScienceCalendar(Session(2016, Season.FALL),
                                          URL("http://calendar.artsci.utoronto.ca"))

    print('getting department calendars')
    deps = cal.get_department_calendars()

    course_datas = []

    print('getting course datas')
    for dep in deps:
        for course in dep.get_courses():
            course_datas.append(course.to_data())

    return {"courses": course_datas}

def create_course_json():
    write_data(_create_course_data(), "data/courses.json")
    print('course data written')

def _create_department_data():
    cal = FacultyOfArtsAndScienceCalendar(Session(2016, Season.FALL),
                                          URL("http://calendar.artsci.utoronto.ca"))
    print('getting department calendars')
    departments = [department.name for department in cal.get_departments()]

    return {"departments": departments}

def create_department_json():
    write_data(_create_department_data(), "data/departments.json")
    print('department data written')

def create_data_json():
    courses = _create_course_data()
    departments = _create_department_data()
    distribution_requirements = {"distribution_requirements": ["Humanity", "Science", "Social Science"]}
    breadth_requirements = {"breadth_requirements": ["1. Creative and Cultural Representations", "2. Thought, Belief, and Behaviour", "3. Society and Its Institutions", "4. Living Things and Their Environment", "5. The Physical and Mathematical Universes"]}
    data = {**courses, **departments, **distribution_requirements, **breadth_requirements}
    write_data(data, "data/data.json")
