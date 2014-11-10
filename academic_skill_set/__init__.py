from itertools import groupby
import nltk
import numpy
from collections import namedtuple


def skill_set(tokenized_exam_results):
    keyword_ranker = KeywordWordFrequencyRanker()
    word_scores = keyword_ranker.word_scores(tokenized_exam_results)
    return map(
        map_rank_tuples_to_ranked_course_keyword,
        merge_ranks(
            rank_tokens_for_courses2(
                word_scores,
                tokenized_exam_results
            )
        )
    )


def map_rank_tuples_to_ranked_course_keyword(ranks):
    return RankedCourseKeyword(
        ranks[0],
        ranks[1],
        ranks[2]
    )


class KeywordWordFrequencyRanker(object):
    def word_scores(self, tokenized_course_exam_results):
        all_chunks = reduce(
            lambda x, y: x + y,
            map(lambda x: x.tokens, tokenized_course_exam_results)
        )
        tokenized_chunks = map(
            lambda x: nltk.word_tokenize(x),
            all_chunks
        )
        return self._calculate_word_scores(tokenized_chunks)


    def _calculate_word_scores(self, phrase_list):
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
        grade_score = grade / 8.5 # Hard coded average_score
    grade_ranked_chunk_scores = [(word, rank*grade_score, course) for word, rank
                                 in chunk_scores.items()]
    return sorted(grade_ranked_chunk_scores, key=lambda x: -x[1])


def _average_chunk_scores(chunk_scores):
    average_score = numpy.average([score for word, score in chunk_scores.items()])
    return dict([(word, score - average_score) for word, score in chunk_scores.items()])





def rank_tokens_for_courses2(word_scores, tokenized_course_exam_results):
    ranked_tokens = map(
        lambda ex_res: rank_tokens_for_course2(word_scores, ex_res),
        tokenized_course_exam_results
    )
    return sorted(reduce(lambda x,y: x + y, ranked_tokens), key=lambda x: -x[1])


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


def _calculate_phrase_scores(phrase_list, word_scores):
    phrase_scores = {}
    for phrase in phrase_list:
      phrase_score = 0
      for word in phrase:
        word_word_score = word_scores[word]
        phrase_score += word_word_score
      phrase_scores[" ".join(phrase)] = phrase_score
    return phrase_scores

RankedCourseKeyword = namedtuple("RankedCourseKeyword",
                                 ['keyword', 'rank', 'course_numbers'])

