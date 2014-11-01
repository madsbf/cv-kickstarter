import sys
sys.path.append('cv_kickstarter/models')

from mock import MagicMock

from grade_average_calculator import GradeAverageCalculator


def test_grade_average_is_calculated_correctly():
    assert GradeAverageCalculator([
        MagicMock(ects_points=7.5, grade=12),
        MagicMock(ects_points=5.0, grade=7),
        MagicMock(ects_points=10.0, grade=4)
    ]).average_grade() == 7.3
    assert GradeAverageCalculator([
        MagicMock(ects_points=10.0, grade=10),
        MagicMock(ects_points=7.5, grade=-3),
        MagicMock(ects_points=5.0, grade=2),
        MagicMock(ects_points=17.5, grade=0)
    ]).average_grade() == 2.2


def test_grade_average_class_method_version():
    assert GradeAverageCalculator([
        MagicMock(ects_points=10.0, grade=10),
        MagicMock(ects_points=5.0, grade=7)
    ]).average_grade() == 9.0


def test_grade_average_with_no_exam_results():
    assert GradeAverageCalculator([]).average_grade() is None


def test_grade_average_ignores_results_without_grade():
    assert GradeAverageCalculator([
        MagicMock(ects_points=10.0, grade=4),
        MagicMock(ects_points=7.5, grade=0),
        MagicMock(ects_points=10.0, grade='BE')
    ]).average_grade() == 2.3
