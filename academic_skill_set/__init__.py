from itertools import groupby
import nltk
import numpy
from collections import namedtuple
import ects_average_grade


def skill_set(tokenized_exam_results):
    return StudentSkillSet().skill_set(tokenized_exam_results)


class StudentSkillSet(object):
    def skill_set(self, tokenized_exam_results):
        keyword_ranker = WordFrequencyScoreCalculator()
        word_scores = keyword_ranker.word_scores(tokenized_exam_results)
        exam_results = map(lambda ter: ter.exam_result, tokenized_exam_results)
        average_grade = ects_average_grade.average_grade(exam_results)
        grade_booster = KeywordGradeBooster(average_grade)
        course_kewords = self._rank_tokens_for_courses2(
            word_scores,
            tokenized_exam_results,
            grade_booster
        )
        course_skills = reduce(lambda x, y: x + y, course_kewords)
        student_skill_set = CourseSkillSetMerger().student_skill_set(
            course_skills
        )
        return self._course_keywords_sorted_by_rank(student_skill_set)

    def _course_keywords_sorted_by_rank(self, student_skill_set):
        return sorted(
            student_skill_set,
            key=lambda course_keyword: -course_keyword.rank
        )

    def _rank_tokens_for_courses2(self, word_scores,
                                  tokenized_course_exam_results,
                                  grade_booster):
        return map(
            CourseSkillSet(grade_booster, word_scores).skill_set,
            tokenized_course_exam_results
        )


class CourseSkillSet(object):
    def __init__(self, grade_booster, word_scores):
        self.grade_booster = grade_booster
        self.word_scores = word_scores

    def skill_set(self, tokenized_exam_result):
        return self.grade_booster.boosted_keyword_scores(
            tokenized_exam_result,
            self._normalized_keyword_scores(tokenized_exam_result)
        )

    def _normalized_keyword_scores(self, tokenized_exam_result):
        return KeywordScoreNormalizer().normalized_keyword_scores(
            self._keyword_scores(tokenized_exam_result)
        )

    def _keyword_scores(self, tokenized_exam_result):
        return KeywordScoreCalculator().keyword_scores(
            tokenized_exam_result,
            self.word_scores
        )


class CourseSkillSetMerger(object):
    def student_skill_set(self, passed_courses_skills):
        sorted_courses_skills = sorted(
            passed_courses_skills,
            key=lambda skill: skill.keyword
        )
        skills_grouped_by_word = groupby(sorted_courses_skills,
                                         lambda x: x.keyword)
        course_keyword_grouped_by_word = [list(course_keyword)
                                          for word, course_keyword
                                          in skills_grouped_by_word]
        return map(self._merge_grouped_ranks, course_keyword_grouped_by_word)

    def _merge_grouped_ranks(self, course_keywords):
        return reduce(
            lambda prevres, next: CourseKeyword(
                next.keyword,
                next.rank + prevres.rank,
                next.course_numbers + prevres.course_numbers
            ),
            course_keywords,
            CourseKeyword('', 0.0, [])
        )


class KeywordScoreCalculator(object):
    def keyword_scores(self, tokenized_exam_result, word_scores):
        tokenized_tokens = map(
            lambda x: nltk.word_tokenize(x),
            tokenized_exam_result.tokens
        )
        return [CourseKeyword(
            " ".join(keyword),
            self._calculate_phrase_scores(keyword, word_scores),
            [tokenized_exam_result.course]
        ) for keyword in tokenized_tokens]

    def _calculate_phrase_scores(self, phrase_tokens, word_scores):
        phrase_score = 0
        for word in phrase_tokens:
            word_word_score = word_scores[word]
            phrase_score += word_word_score
        return phrase_score


class KeywordGradeBooster(object):
    def __init__(self, average_grade):
        self.average_grade = average_grade

    def boosted_keyword_scores(self, tokenized_exam_result, scored_keywords):
        return list(map(
            lambda keyword: self._boosted_course_keyword(
                keyword,
                tokenized_exam_result and tokenized_exam_result.course,
                tokenized_exam_result.exam_result.grade
            ),
            scored_keywords
        ))

    def _boosted_course_keyword(self, scored_keyword, course, grade):
        return CourseKeyword(
            scored_keyword.keyword,
            self._boosted_keyword_score(scored_keyword.rank, grade),
            scored_keyword.course_numbers
        )

    def _boosted_keyword_score(self, keyword_score, grade):
        return keyword_score * self._grade_score(grade)

    def _grade_score(self, grade):
        if type(grade) is not float:
            return 1.0
        return grade / self.average_grade


class KeywordScoreNormalizer(object):
    def normalized_keyword_scores(self, keyword_scores):
        average_score = numpy.average(
            [keyword_score.rank for keyword_score in keyword_scores]
        )
        return list(map(
            lambda old_score: CourseKeyword(
                old_score.keyword,
                self._normalized_score(old_score.rank, average_score),
                old_score.course_numbers
            ),
            keyword_scores
        ))

    def _normalized_score(self, score, average):
        return score / average


class WordFrequencyScoreCalculator(object):
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
            degree = len(phrase)
            for word in phrase:
                word_freq[word] += 1
                word_degree[word] += degree
        for word in word_freq.keys():
            word_degree[word] = word_degree[word] + word_freq[word]
        word_scores = {}
        for word in word_freq.keys():
            word_scores[word] = word_degree[word] / word_freq[word]
        return word_scores


CourseKeyword = namedtuple("CourseKeyword",
                           ['keyword', 'rank', 'course_numbers'])
