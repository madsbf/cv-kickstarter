from __future__ import division

import sys
from collections import namedtuple

sys.path.append('cv_kickstarter/lib')
sys.path.append('cv_kickstarter/models')

import academic_skill_set
from course_keyword_tokenizer import CourseKeywordTokenizer
from campus_net_course_base_merger import CampusNetCourseBaseMerger


class DtuSkillSet(object):
    def __init__(self, exam_result_programmes, course_base_repo):
        self.exam_result_programmes = exam_result_programmes
        self.course_base_repo = course_base_repo

    def skill_set(self):
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
            CourseKeywordTokenizer(exam_result.course).tokens(),
            exam_result.course
        )

TokenizedCourseExamResult = namedtuple(
    "TokenizedCourseExamResult",
    ['exam_result', 'tokens', 'course']
)
