import nltk


class CourseSentenceExtractor(object):
    def __init__(self, course):
        self.course = course

    def sentences(self):
        return reduce(
            lambda x, y: x + y,
            map(lambda x: nltk.sent_tokenize(x), self._course_texts())
        )

    def _course_texts(self):
        return [
            self.course.title,
            self.course.contents,
            self.course.course_objectives_text
        ] + list(self.course.course_objectives)
