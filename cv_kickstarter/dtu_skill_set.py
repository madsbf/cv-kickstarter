"""Extract the skill set of a DTU student.

This module is a layer on top of academic_skill_set that takes exam results
as given by the CampusNet API, merges it with course information from
the Course Base (through the course base repo).
"""
from functools import reduce
from collections import namedtuple
from cv_kickstarter import academic_skill_set


class DtuSkillSet(object):

    """Responsible for extracting a skill set based on DTU data sources."""

    def __init__(self, exam_result_programmes, course_base_repo):
        """Initialize DtuSkillSet with exam results and course repo.

        The exam_result_programmes are as they come from the cnapi. The
        course base repo (or repository) should be able to find courses
        from the course base.
        """
        self.exam_result_programmes = exam_result_programmes
        self.course_base_repo = course_base_repo

    def skill_set(self):
        """Return the skill set."""
        return academic_skill_set.skill_set(self._tokenized_exam_results())

    def _tokenized_exam_results(self):
        return map(
            self._map_to_tokenized_exam_result,
            self._course_exam_results()
        )

    def _course_exam_results(self):
        return CampusNetCourseBaseMerger(
            self.exam_result_programmes,
            self.course_base_repo
        ).course_exam_results()

    def _map_to_tokenized_exam_result(self, exam_result):
        return TokenizedCourseExamResult(
            exam_result,
            exam_result.course_tokens,
            exam_result.course
        )

TokenizedCourseExamResult = namedtuple(
    "TokenizedCourseExamResult",
    ['exam_result', 'tokens', 'course']
)
