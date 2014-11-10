from __future__ import division

import sys

sys.path.append('cv_kickstarter/lib')
sys.path.append('cv_kickstarter/models')

import academic_skill_set

from xml_course_base_repo_builder import XmlCourseBaseRepoBuilder
from course_keyword_tokenizer import CourseKeywordTokenizer
from campus_net_course_base_merger import CampusNetCourseBaseMerger


def final_keywords(grades):
    exam_results = course_exam_results(grades)
    tokenized_courses = map(tokenized_course_exam_result, exam_results)
    # word_scores = global_word_score(tokenized_courses)
    # return map(
    #     map_rank_tuples_to_ranked_course_keyword,
    #     merge_ranks(
    #         rank_tokens_for_courses2(
    #             word_scores,
    #             tokenized_courses
    #         )
    #     )
    # )
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
        CourseKeywordTokenizer(exam_result.course).tokens()
    )


class TokenizedCourseExamResult(object):
    def __init__(self, exam_result, tokens):
        self.exam_result = exam_result
        self.tokens = tokens

    @property
    def course(self):
        return self.exam_result.course

# def rank_tokens_for_courses():
#     ranked_tokens = map(
#         rank_tokens_for_course,
#         tokenized_courses()
#     )
#     return sorted(reduce(lambda x,y: x + y, ranked_tokens), key=lambda x: -x[1])

# def rank_tokens_for_course(tokenized_course_exam_result):
#     tokenized_tokens = map(
#         lambda x: nltk.word_tokenize(x),
#         tokenized_course_exam_result.tokens
#     )
#     word_scores = _calculate_word_scores(tokenized_tokens)
#     chunk_scores = _calculate_phrase_scores(tokenized_tokens, word_scores)
#     grade = tokenized_course_exam_result.exam_result.grade
#     grade_score = 1.0
#     if type(grade) is float or type(grade) is int:
#         grade_score = grade / 8.5
#     grade_ranked_chunk_scores = [(word, rank*grade_score) for word, rank
#                                  in chunk_scores.items()]
#     return sorted(grade_ranked_chunk_scores, key=lambda x: -x[1])
