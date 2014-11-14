import ects_average_grade


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
        return ects_average_grade.average_grade(self.exam_results)

    def _has_passed(self, ects_points):
        return self.passed_ects >= ects_points
