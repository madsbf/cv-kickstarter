from werkzeug import cached_property
from user_cv import UserCV
from exam_result_programme import ExamResultProgramme
from exam_result import ExamResult


class UserCVBuilder(object):

    def __init__(self, campus_net_client):
        self.campus_net_client = campus_net_client

    def build(self):
        return UserCV(
            self.user.first_name,
            self.user.last_name,
            self.grades
        )

    @cached_property
    def user(self):
        return self.campus_net_client.user()

    @cached_property
    def grades(self):
        return map(
            self._map_exam_result_programme,
            self.campus_net_client.grades()
        )

    def _map_exam_result_programme(self, exam_result_programme):
        return ExamResultProgramme(
            exam_result_programme.name,
            exam_result_programme.passed_ects_points,
            map(self._map_exam_results, exam_result_programme.exam_results)
        )

    def _map_exam_results(self, exam_result):
        return ExamResult(exam_result)
