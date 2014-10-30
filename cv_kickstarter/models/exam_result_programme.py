import re


class ExamResultProgramme(object):
    def __init__(self, name, passed_ects_points, exam_results):
        self.name = name
        self.passed_ects_points = passed_ects_points
        self.exam_results = exam_results

    @property
    def is_done(self):
        if re.search(r"Bachelor", self.name):
            return self._has_passed(180.0)
        elif re.search(r"Master", self.name):
            return self._has_passed(120.0)

    def _has_passed(self, ects_points):
        return self.passed_ects_points >= ects_points
