from cv_kickstarter.models.exam_result_programme import ExamResultProgramme
import re


class CampusNetExamResultMapper(object):
    def __init__(self, cn_exam_result_programme):
        self.cn_exam_result_programme = cn_exam_result_programme

    def mapped_exam_result(self):
        return ExamResultProgramme(
            self.cn_exam_result_programme.name,
            self.cn_exam_result_programme.passed_ects_points,
            self._total_programme_ects(self.cn_exam_result_programme.name),
            self.cn_exam_result_programme.exam_results
        )

    def _total_programme_ects(self, programme_name):
        if re.search(r"Bachelor", programme_name):
            return 180.0
        elif re.search(r"Master|Kandidat", programme_name):
            return 120.0
