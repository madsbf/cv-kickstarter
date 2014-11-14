from mock import MagicMock
import ects_grade_calculator


def test_grade_average_is_calculated_correctly():
    assert ects_grade_calculator.average_grade([
        MagicMock(ects_points=7.5, grade=12),
        MagicMock(ects_points=5.0, grade=7),
        MagicMock(ects_points=10.0, grade=4)
    ]) == 7.3
    assert ects_grade_calculator.average_grade([
        MagicMock(ects_points=10.0, grade=10),
        MagicMock(ects_points=7.5, grade=-3),
        MagicMock(ects_points=5.0, grade=2),
        MagicMock(ects_points=17.5, grade=0)
    ]) == 2.2


def test_grade_average_class_method_version():
    assert ects_grade_calculator.average_grade([
        MagicMock(ects_points=10.0, grade=10),
        MagicMock(ects_points=5.0, grade=7)
    ]) == 9.0


def test_grade_average_with_no_exam_results():
    assert ects_grade_calculator.average_grade([]) is None


def test_grade_average_ignores_results_without_grade():
    assert ects_grade_calculator.average_grade([
        MagicMock(ects_points=10.0, grade=4),
        MagicMock(ects_points=7.5, grade=0),
        MagicMock(ects_points=10.0, grade='BE')
    ]) == 2.3


def test_grade_average_without_meaningful_grades():
    assert ects_grade_calculator.average_grade([
        MagicMock(ects_points=10.0, grade='BE')
    ]) is None
