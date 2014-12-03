"""Extracts a skill set based on keywords in exam results.

AcademicSkillSet extracts a skill set based on keywords in the exam results.

The keywords are ranked by the freqency and grades.
"""

from itertools import groupby
from functools import reduce
import nltk
import numpy
from collections import namedtuple
from cv_kickstarter import ects_grade_calculator

from cv_kickstarter import nltk_data_downloader

nltk_data_downloader.download()


def skill_set(tokenized_exam_results,
              min_keyword_length=4):
    """Extract skill set based on tokenized exam results.

    Tokenized exam results are exam results with tokens for each course.

    Optimal arguments are
        min_keyword_length: The minimum amount of characters in a keyword

    The last max_keyword_courses is used for filtering away keywords that
    are too common in the courses (e.g. 'course', 'analysis').
    """
    return StudentSkillSet(
        WordFrequencyScoreCalculator(),
        _build_grade_booster(tokenized_exam_results),
        StudentSkillSetNoiceFilter(min_keyword_length)
    ).skill_set(tokenized_exam_results)


def _build_grade_booster(tokenized_exam_results):
    exam_results = list(
        map(lambda ter: ter.exam_result, tokenized_exam_results)
    )
    average_grade = ects_grade_calculator.average_grade(exam_results)
    grade_booster = KeywordGradeBooster(average_grade)
    return grade_booster


class StudentSkillSetNoiceFilter(object):

    """Filters away noice from the skill set.

    Filters away noice meaning unwanted keywords in the skill set.
    """

    def __init__(self, min_keyword_length):
        """Initialize with min_keyword_length.

        min_keyword_length: The minimum amount of characters in a keyword
        """
        self.min_keyword_length = min_keyword_length

    def filtered_skill_set(self, course_keywords):
        """Return a filtered set of skills."""
        return filter(self._valid_keyword, course_keywords)

    def _valid_keyword(self, keyword):
        return len(keyword.keyword) >= self.min_keyword_length


class StudentSkillSet(object):

    """Extract skill set of a student."""

    def __init__(self, word_scorer, grade_booster, noice_filter):
        """Initialize with word_scorer, grade_booster and noice_filter."""
        self.word_scorer = word_scorer
        self.grade_booster = grade_booster
        self.noice_filter = noice_filter

    def skill_set(self, tokenized_exam_results):
        """Return a ranked skill set."""
        course_kewords = self._rank_tokens_for_courses2(
            tokenized_exam_results,
            self.grade_booster
        )
        course_skills = reduce(lambda x, y: x + y, course_kewords)
        student_skill_set = CourseSkillSetMerger().student_skill_set(
            course_skills
        )
        return self.noice_filter.filtered_skill_set(
            self._course_keywords_sorted_by_rank(student_skill_set)
        )

    def _course_keywords_sorted_by_rank(self, student_skill_set):
        return sorted(
            student_skill_set,
            key=lambda course_keyword: -course_keyword.rank
        )

    def _rank_tokens_for_courses2(self, tokenized_course_exam_results,
                                  grade_booster):
        return map(
            CourseSkillSet(grade_booster, self.word_scorer).skill_set,
            tokenized_course_exam_results
        )


class CourseSkillSet(object):

    """Extract skill gained in a given course."""

    def __init__(self, grade_booster, word_scorer):
        """Initialize with a grade_booster and word_scorer dictionary."""
        self.grade_booster = grade_booster
        self.word_scorer = word_scorer

    def skill_set(self, tokenized_exam_result):
        """Return a skill set gained in the given course."""
        return self.grade_booster.boosted_keyword_scores(
            tokenized_exam_result,
            self._normalized_keyword_score(tokenized_exam_result)
        )

    def _normalized_keyword_score(self, tokenized_exam_result):
        return KeywordScoreNormalizer().normalized_keyword_score(
            self._keyword_scorer(tokenized_exam_result)
        )

    def _keyword_scorer(self, tokenized_exam_result):
        return KeywordScoreCalculator().keyword_scorer(
            tokenized_exam_result,
            self.word_scorer
        )


class CourseSkillSetMerger(object):

    """Merges skill sets from several courses into a common skill set."""

    def student_skill_set(self, passed_courses_skills):
        """Return a raw skill set merged.

        Each course skill set is merged, which means that common skills from
        the different courses arge merged into one CourseKeyword, which
        lists both courses.

        For keywords contained in two course skill sets, the rank is summed as
        the keyword gained in more courses are considered more important.
        """
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

    """"Calculates the raw keyword scores based on the word scores."""

    def keyword_scorer(self, tokenized_exam_result, word_scorer):
        """"Return keyword scores."""
        word_scores = word_scorer.word_scorer(tokenized_exam_result)
        tokenized_tokens = map(
            lambda x: nltk.word_tokenize(x),
            list(set(tokenized_exam_result.tokens))
        )
        return [CourseKeyword(
            " ".join(keyword),
            self._calculate_phrase_scores(keyword, word_scores),
            [tokenized_exam_result.course]
        ) for keyword in tokenized_tokens]

    def _calculate_phrase_scores(self, phrase_tokens, word_scores):
        return sum(word_scores[word] for word in phrase_tokens)


class KeywordGradeBooster(object):

    """Boosts the keyword rank with the grade.

    Multiplies the given keyword rank score with a grade score from the course
    the course originated.
    """

    def __init__(self, average_grade):
        """Initialize with the average_grade of the student."""
        self.average_grade = average_grade

    def boosted_keyword_scores(self, tokenized_exam_result, scored_keywords):
        """Return a list of keywords with a rank boosted by grade."""
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
        if type(grade) is not int:
            return 1.0
        return grade / self.average_grade


class KeywordScoreNormalizer(object):

    """Normalize the rank score of a keyword with average score in course."""

    def normalized_keyword_score(self, keyword_scorer):
        """Return a list of keywords with rank divided by average rank."""
        ranks = [keyword_score.rank for keyword_score in keyword_scorer]
        average_score = numpy.average(ranks)
        score_std = numpy.std(ranks)
        return list(map(
            lambda old_score: CourseKeyword(
                old_score.keyword,
                self._normalized_score(
                    old_score.rank,
                    average_score,
                    score_std),
                old_score.course_numbers
            ),
            keyword_scorer
        ))

    def _normalized_score(self, score, average, std):
        return (score - average) / std


class WordFrequencyScoreCalculator(object):

    """Builds a word score dictionary based on word frequency."""

    def word_scorer(self, tokenized_course_exam_result):
        """Return a dictionary of word scores.

        The score for each word is the frequency of the word in all
        exam results.
        """
        tokenized_chunks = map(
            lambda x: nltk.word_tokenize(x),
            tokenized_course_exam_result.tokens
        )
        return self._calculate_word_scorer(tokenized_chunks)

    def _calculate_word_scorer(self, phrase_list):
        words = [word for phrase in phrase_list for word in phrase]
        return dict(nltk.FreqDist(words).items())

CourseKeyword = namedtuple("CourseKeyword",
                           ['keyword', 'rank', 'course_numbers'])
