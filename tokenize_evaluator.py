from __future__ import division

import sys
from collections import namedtuple

sys.path.append('cv_kickstarter/lib')
sys.path.append('cv_kickstarter/models')

import academic_skill_set

from xml_course_base_repo_builder import XmlCourseBaseRepoBuilder
from course_keyword_tokenizer import CourseKeywordTokenizer
from campus_net_course_base_merger import CampusNetCourseBaseMerger


def final_keywords(grades):
    exam_results = course_exam_results(grades)
    tokenized_courses = map(tokenized_course_exam_result, exam_results)
    return academic_skill_set.skill_set(tokenized_courses)


def course_exam_results(exam_result_programmes):
    course_base = XmlCourseBaseRepoBuilder(
        'courses.xml'
    ).course_base_repo()

    return CampusNetCourseBaseMerger(
        exam_result_programmes,
        course_base
    ).course_exam_results()


def tokenized_course_exam_result(exam_result):
    return TokenizedCourseExamResult(
        exam_result,
        CourseKeywordTokenizer(exam_result.course).tokens(),
        exam_result.course
    )

TokenizedCourseExamResult = namedtuple(
    "TokenizedCourseExamResult",
    ['exam_result', 'tokens', 'course']
)
