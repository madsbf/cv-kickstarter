import sys
sys.path.append('cv_kickstarter/models')

from course_exam_result_builder import CourseExamResultBuilder, ExamResult
from mock import Mock, MagicMock
from pytest import yield_fixture


class FakeCourseBase(object):
    def __init__(self):
        self.course = None

    def find_by_course_number(self, course_number):
        return self.course


@yield_fixture
def fake_course_base():
    yield FakeCourseBase()


@yield_fixture
def good_exam_result():
    yield MagicMock(grade=12, course_number='02819')


def test_exam_result_with_correct_paramters(monkeypatch, fake_course_base,
                                            good_exam_result):
    course = MagicMock()
    fake_course_base.course = course
    exam_result_init = Mock(return_value=None)
    monkeypatch.setattr(ExamResult, '__init__', exam_result_init)
    CourseExamResultBuilder(
        good_exam_result,
        fake_course_base
    ).course_exam_result()
    exam_result_init.assert_called_with(12, course)


def test_exam_result_object_is_returned(fake_course_base, good_exam_result):
    course_exam_result = CourseExamResultBuilder(
        good_exam_result,
        fake_course_base
    ).course_exam_result()
    assert type(course_exam_result) == ExamResult
