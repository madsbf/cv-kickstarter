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
            self._passed_course_exam_results()
        )

    def _passed_course_exam_results(self):
        return [exam_result for exam_result
                in self._course_exam_results() if exam_result.grade != 'EM']

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


class CampusNetCourseBaseMerger(object):

    """Merges exam results with information about the course."""

    def __init__(self, exam_result_programmes, course_base):
        """Initialize with exam results and course base."""
        self.exam_result_programmes = exam_result_programmes
        self.course_base = course_base

    def course_exam_results(self):
        """Return course exam results.

        A list of ExamResult, that contains exam result information and
        more detailed information about the course given by the returned
        course object from course base.
        """
        return list(map(
            self._map_campus_net_exam_result,
            self._campus_net_exam_results()
        ))

    def _map_campus_net_exam_result(self, exam_result):
        return ExamResult(
            exam_result.grade,
            self.course_base.find_by_course_number(
                exam_result.course_number
            ),
            exam_result.ects_points
        )

    def _campus_net_exam_results(self):
        return reduce(
            lambda x, y: x + y,
            map(
                lambda x: x.exam_results,
                self.exam_result_programmes
            ),
            []
        )


class ExamResult(object):

    """Exam result with grade, course and ects points."""

    def __init__(self, grade, course, ects_points):
        """Initialize with grade, course and ects_points."""
        self.grade = grade
        self.course = course
        self.ects_points = ects_points

    @property
    def course_tokens(self):
        """Return the tokens of the course."""
        if self.course is None:
            return []
        return self.course.tokens


TokenizedCourseExamResult = namedtuple(
    "TokenizedCourseExamResult",
    ['exam_result', 'tokens', 'course']
)
