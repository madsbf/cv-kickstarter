from functools import reduce
import nltk
from cv_kickstarter import nltk_data_downloader

nltk_data_downloader.download()


def course_tokens(course):
    return CourseKeywordTokenizer(course).tokens()


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


class CourseSentenceExtractor(object):
    def __init__(self, course):
        self.course = course

    def sentences(self):
        return reduce(
            lambda x, y: x + y,
            map(lambda x: nltk.sent_tokenize(x), self._course_texts()),
            []
        )

    def _course_texts(self):
        return [
            self.course.title,
            self.course.contents,
            self.course.course_objectives_text
        ] + list(self.course.course_objectives)


# Inspired by Finn Nielsens code from Data Mining using Python 02819 at DTU.
class TextChunkifier(object):
    def text_chunks(self, text):
        return self._extract_chunks(
            self._grammar_parser().parse(
                nltk.pos_tag(
                    nltk.word_tokenize(text)
                )
            )
        )

    def _extract_chunks(self, tree, tree_filter='NP'):
        chunks = []
        if hasattr(tree, 'label'):
            if tree.label() == tree_filter:
                leafWords = map(self._extract_word_from_leaf, tree.leaves())
                chunks = [" ".join(leafWords)]
            else:
                for child in tree:
                    cs = self._extract_chunks(child, tree_filter=tree_filter)
                    if cs != []:
                        chunks.append(cs[0])
        return chunks

    def _extract_word_from_leaf(self, leaf):
        return leaf[0].lower()

    def _grammar_parser(self):
        return nltk.RegexpParser("NP: { <JJ>*<NN.?>+ }")
