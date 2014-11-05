import sys
sys.path.append('cv_kickstarter/lib')

from course_base_repo import CourseBaseRepo
from mock import MagicMock


def test_course_found_by_course_number():
    data_mining_with_python = MagicMock(course_number='02819')
    courses = [
        data_mining_with_python,
        MagicMock(course_number='01227')
    ]
    course_result = CourseBaseRepo(courses).find_by_course_number('02819')
    assert course_result == data_mining_with_python


def test_course_not_found_by_course_number_returns_none():
    courses = [
        MagicMock(course_number='02819'),
        MagicMock(course_number='01227')
    ]
    course_result = CourseBaseRepo(courses).find_by_course_number('01005')
    assert course_result is None
