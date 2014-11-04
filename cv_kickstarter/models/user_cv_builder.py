from werkzeug import cached_property
from user_cv import UserCV
from campus_net_exam_result_mapper import CampusNetExamResultMapper


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
        return list(map(
            self._map_exam_result_programme,
            self.campus_net_client.grades()
        ))

    def _map_exam_result_programme(self, exam_result):
        return CampusNetExamResultMapper(
            exam_result
        ).mapped_exam_result()
