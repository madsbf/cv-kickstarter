import re
from exam_result import ExamResult


class ExamResultProgramme(object):
    def __init__(self, programme):
        self.programme = programme

    @property
    def name(self):
        return self.programme.name

    @property
    def exam_results(self):
        return map(ExamResult, self.programme.exam_results)

    @property
    def is_done(self):
        if re.search(r"Bachelor", self.programme.name):
            return self._has_passed(180.0)
        elif re.search(r"Master", self.programme.name):
            return self._has_passed(120.0)

    def _has_passed(self, ects_points):
        return self.programme.passed_ects_points >= ects_points
