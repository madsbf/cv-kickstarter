import sys
sys.path.append('cv_kickstarter/models')

from exam_result_programme import ExamResultProgramme


def test_is_done_when_passed_ects_is_equal_to_total_ects():
    programme = ExamResultProgramme('ProgName', 120.0, 120.0, [])
    assert programme.is_done is True


def test_is_not_done_when_passed_ects_is_equal_to_total_ects():
    programme = ExamResultProgramme('ProgName', 70.0, 120.0, [])
    assert programme.is_done is False
