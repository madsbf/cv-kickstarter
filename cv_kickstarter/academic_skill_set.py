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
              min_keyword_length=4,
              max_keyword_courses=6):
    """Extract skill set based on tokenized exam results.

    Tokenized exam results are exam results with tokens for each course.

    Optimal arguments are
        min_keyword_length: The minimum amount of characters in a keyword
        max_keyword_courses: The maximum amount of courses for a keyword

    The last max_keyword_courses is used for filtering away keywords that
    are too common in the courses (e.g. 'course', 'analysis').
    """
    return StudentSkillSet(
        WordFrequencyScoreCalculator().word_scores(tokenized_exam_results),
        _build_grade_booster(tokenized_exam_results),
        StudentSkillSetNoiceFilter(
            min_keyword_length,
            max_keyword_courses
        )
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

    def __init__(self, min_keyword_length, max_keyword_courses):
        """Initialize with min_keyword_length and max_keyword_courses.

        min_keyword_length: The minimum amount of characters in a keyword
        max_keyword_courses: The maximum amount of courses for a keyword
        """
        self.min_keyword_length = min_keyword_length
        self.max_keyword_courses = max_keyword_courses

    def filtered_skill_set(self, course_keywords):
        """Return a filtered set of skills."""
        return filter(self._valid_keyword, course_keywords)

    def _valid_keyword(self, keyword):
        return (len(keyword.course_numbers) <= self.min_keyword_length
                and len(keyword.keyword) >= self.max_keyword_courses)


class StudentSkillSet(object):

    """Extract skill set of a student."""

    def __init__(self, word_scores, grade_booster, noice_filter):
        """Initialize with word_scores, grade_booster and noice_filter."""
        self.word_scores = word_scores
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
            CourseSkillSet(grade_booster, self.word_scores).skill_set,
            tokenized_course_exam_results
        )


class CourseSkillSet(object):

    """Extract skill gained in a given course."""

    def __init__(self, grade_booster, word_scores):
        """Initialize with a grade_booster and word_scores dictionary."""
        self.grade_booster = grade_booster
        self.word_scores = word_scores

    def skill_set(self, tokenized_exam_result):
        """Return a skill set gained in the given course."""
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

    def keyword_scores(self, tokenized_exam_result, word_scores):
        """"Return keyword scores."""
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

    def normalized_keyword_scores(self, keyword_scores):
        """Return a list of keywords with rank divided by average rank."""
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

    """Builds a word score dictionary based on word frequency."""

    def word_scores(self, tokenized_course_exam_results):
        """Return a dictionary of word scores.

        The score for each word is the frequency of the word in all
        exam results.
        """
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
        words = [word for phrase in phrase_list for word in phrase]
        return dict(nltk.FreqDist(words).items())

CourseKeyword = namedtuple("CourseKeyword",
                           ['keyword', 'rank', 'course_numbers'])
