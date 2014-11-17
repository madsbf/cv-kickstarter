from functools import reduce
from text_chunkifier import TextChunkifier
from course_sentence_extractor import CourseSentenceExtractor


class CourseKeywordTokenizer(object):
    def __init__(self, course):
        self.course = course

    def tokens(self):
        if self.course is None:
            return []
        return reduce(
            lambda x, y: x + y,
            map(TextChunkifier().text_chunks, self._course_sentences()),
            []
        )

    def _course_sentences(self):
        return CourseSentenceExtractor(self.course).sentences()
