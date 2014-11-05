from __future__ import division

import nltk
import sys
import numpy

sys.path.append('cv_kickstarter/lib')
sys.path.append('cv_kickstarter/models')
sys.path.append('dtu_course_base')

import base64
import cnapi
import dtu_course_base
from werkzeug import cached_property

from course_keyword_tokenizer import CourseKeywordTokenizer
from course_base_repo import CourseBaseRepo
from campus_net_course_base_merger import CampusNetCourseBaseMerger


def final_keywords(grades):
    exam_results = course_exam_results(grades)
    tokenized_courses = map(tokenized_course_exam_result, exam_results)
    word_scores = global_word_score(tokenized_courses)
    return map(
        map_rank_tuples_to_ranked_course_keyword,
        merge_ranks(
            rank_tokens_for_courses2(
                word_scores,
                tokenized_courses
            )
        )
    )

def map_rank_tuples_to_ranked_course_keyword(ranks):
    return RankedCourseKeyword(
        ranks[0],
        ranks[1],
        ranks[2]
    )

class RankedCourseKeyword(object):
    def __init__(self, keyword, rank, course_numbers):
        self.keyword = keyword
        self.rank = rank
        self.course_numbers = course_numbers


def course_exam_results(exam_result_programmes):
    course_base = XmlCourseBaseRepositoryBuilder(
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


def rank_tokens_for_courses():
    ranked_tokens = map(
        rank_tokens_for_course,
        tokenized_courses()
    )
    return sorted(reduce(lambda x,y: x + y, ranked_tokens), key=lambda x: -x[1])

def rank_tokens_for_course(tokenized_course_exam_result):
    tokenized_tokens = map(
        lambda x: nltk.word_tokenize(x),
        tokenized_course_exam_result.tokens
    )
    word_scores = _calculate_word_scores(tokenized_tokens)
    chunk_scores = _calculate_phrase_scores(tokenized_tokens, word_scores)
    grade = tokenized_course_exam_result.exam_result.grade
    grade_score = 1.0
    if type(grade) is float or type(grade) is int:
        grade_score = grade / 8.5
    grade_ranked_chunk_scores = [(word, rank*grade_score) for word, rank
                                 in chunk_scores.items()]
    return sorted(grade_ranked_chunk_scores, key=lambda x: -x[1])

def rank_tokens_for_course2(word_scores, tokenized_course_exam_result):
    course = None
    if tokenized_course_exam_result.course:
        course = tokenized_course_exam_result.course
    tokenized_tokens = map(
        lambda x: nltk.word_tokenize(x),
        tokenized_course_exam_result.tokens
    )
    chunk_scores = _calculate_phrase_scores(tokenized_tokens, word_scores)
    chunk_scores = _average_chunk_scores(chunk_scores)
    grade = tokenized_course_exam_result.exam_result.grade
    grade_score = 1.0
    if type(grade) is float or type(grade) is int:
        grade_score = grade / 8.5 # Hard coded average
    grade_ranked_chunk_scores = [(word, rank*grade_score, course) for word, rank
                                 in chunk_scores.items()]
    return sorted(grade_ranked_chunk_scores, key=lambda x: -x[1])


def _average_chunk_scores(chunk_scores):
    average_score = numpy.average([score for word, score in chunk_scores.items()])
    return dict([(word, score - average_score) for word, score in chunk_scores.items()])


def global_word_score(tokenized_course_exam_results):
    all_chunks = reduce(lambda x, y: x + y, map(lambda x: x.tokens, tokenized_course_exam_results))
    tokenized_chunks = map(
        lambda x: nltk.word_tokenize(x),
        all_chunks
    )
    return _calculate_word_scores(tokenized_chunks)


def rank_tokens_for_courses2(word_scores, tokenized_course_exam_results):
    ranked_tokens = map(
        lambda ex_res: rank_tokens_for_course2(word_scores, ex_res),
        tokenized_course_exam_results
    )
    return sorted(reduce(lambda x,y: x + y, ranked_tokens), key=lambda x: -x[1])


from itertools import groupby

def merge_ranks(ranks):
    ranks_grouped_by_word = [list(w) for k, w in groupby(ranks, lambda x: x[0])]
    return map(merge_grouped_ranks, ranks_grouped_by_word)


def merge_grouped_ranks(grouped_ranks):
    return reduce(
        lambda prevres, next: tuple([
            next[0],
            next[1] + prevres[1],
            [next[2]] + prevres[2]
        ]),
        grouped_ranks,
        ('', 0.0, [])
    )

def _calculate_word_scores(phrase_list):
    word_freq = nltk.FreqDist()
    word_degree = nltk.FreqDist()
    for phrase in phrase_list:
      degree = len(phrase) - 1
      for word in phrase:
        word_freq[word] += 1
        word_degree[word] += degree
    for word in word_freq.keys():
      word_degree[word] = word_degree[word] + word_freq[word]
    word_scores = {}
    for word in word_freq.keys():
      word_scores[word] = word_degree[word] / word_freq[word]
    return word_scores


def _calculate_phrase_scores(phrase_list, word_scores):
    phrase_scores = {}
    for phrase in phrase_list:
      phrase_score = 0
      for word in phrase:
        # print(word)
        # print
        word_word_score = word_scores[word]
        phrase_score += word_word_score
      phrase_scores[" ".join(phrase)] = phrase_score
    return phrase_scores


class TokenizedCourseExamResult(object):
    def __init__(self, exam_result, tokens):
        self.exam_result = exam_result
        self.tokens = tokens

    @property
    def course(self):
        return self.exam_result.course


class XmlCourseBaseRepositoryBuilder(object):
    def __init__(self, course_xml_path):
        self.course_xml_path = course_xml_path

    def course_base_repo(self):
        return CourseBaseRepo(self._courses_from_xml())

    def _courses_from_xml(self):
        return dtu_course_base.courses_from_xml(self._course_xml())

    def _course_xml(self):
        return open('courses.xml').read()
