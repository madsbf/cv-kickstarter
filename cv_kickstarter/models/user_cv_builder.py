from werkzeug import cached_property
from cv_kickstarter.models.user_cv import UserCV
from cv_kickstarter.models.campus_net_exam_result_mapper import (
    CampusNetExamResultMapper
)
from cv_kickstarter.course_repository import CourseRepository
from cv_kickstarter.dtu_skill_set import DtuSkillSet


class UserCVBuilder(object):

    def __init__(self, campus_net_client, mongo_store):
        self.campus_net_client = campus_net_client
        self.mongo_store = mongo_store

    def build(self):
        return UserCV(
            self.user.first_name,
            self.user.last_name,
            self.grades,
            self._keywords
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

    @property
    def _keywords(self):
        return DtuSkillSet(
            self.grades,
            self._course_base_repo()
        ).skill_set()

    def _course_base_repo(self):
        return CourseRepository(self.mongo_store)

    def _map_exam_result_programme(self, exam_result):
        return CampusNetExamResultMapper(
            exam_result
        ).mapped_exam_result()
