from grade_average_calculator import GradeAverageCalculator


class ExamResultProgramme(object):
    def __init__(self, name, passed_ects, total_ects, exam_results):
        self.name = name
        self.passed_ects = passed_ects
        self.total_ects = total_ects
        self.exam_results = exam_results

    @property
    def is_done(self):
        return self._has_passed(self.total_ects)

    @property
    def average_grade(self):
        return GradeAverageCalculator(self.exam_results).average_grade()

    def _has_passed(self, ects_points):
        return self.passed_ects >= ects_points

    def _ects_sum_of_graded_courses(self):
        return sum()
