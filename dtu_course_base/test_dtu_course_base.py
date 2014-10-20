import dtu_course_base


def test_course_number_extraction():
    courses_xml = open('small_courses.xml').read()
    courses = dtu_course_base.courses_from_xml(courses_xml)
    first_course = courses[0]
    assert first_course.course_number == '01005'


def test_title_extraction():
    courses_xml = open('small_courses.xml').read()
    courses = dtu_course_base.courses_from_xml(courses_xml)
    first_course = courses[0]
    assert first_course.title == 'Matematik 1'
