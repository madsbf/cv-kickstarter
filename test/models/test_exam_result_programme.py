import sys
sys.path.append('cv_kickstarter/models')

from exam_result_programme import ExamResultProgramme, GradeAverageCalculator


def test_is_done_when_passed_ects_is_equal_to_total_ects():
    programme = ExamResultProgramme('ProgName', 120.0, 120.0, [])
    assert programme.is_done is True


def test_is_not_done_when_passed_ects_is_equal_to_total_ects():
    programme = ExamResultProgramme('ProgName', 70.0, 120.0, [])
    assert programme.is_done is False


def test_average_grade_calculated_with_calculator(monkeypatch):
    programme = ExamResultProgramme('ProgName', 70.0, 120.0, [])
    monkeypatch.setattr(GradeAverageCalculator, 'average_grade',
                        lambda x: 60.0)
    assert programme.average_grade == 60.0
