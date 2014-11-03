from werkzeug import cached_property
from user_cv import UserCV
from exam_result_programme import ExamResultProgramme
import re


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
            self._total_programme_ects(exam_result_programme.name),
            exam_result_programme.exam_results
        )

    def _total_programme_ects(self, programme_name):
        if re.search(r"Bachelor", programme_name):
            return 180.0
        elif re.search(r"Master", programme_name):
            return 120.0
