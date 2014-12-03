"""The exam result programme with exam results for a given programme."""
from cv_kickstarter import ects_grade_calculator


class ExamResultProgramme(object):

    """Representing exam results for a given programme (bachelor, master..)."""

    def __init__(self, name, passed_ects, total_ects, exam_results):
        """Initialize with name, passed_ects, total_ects and exam_results."""
        self.name = name
        self.passed_ects = passed_ects
        self.total_ects = total_ects
        self.exam_results = exam_results

    @property
    def is_done(self):
        """Return true if all the courses are passed for the programme."""
        return self._has_passed(self.total_ects)

    @property
    def average_grade(self):
        """Return the average grade of the student."""
        return ects_grade_calculator.average_grade(self.exam_results)

    def _has_passed(self, ects_points):
        return ects_points is not None and self.passed_ects >= ects_points
