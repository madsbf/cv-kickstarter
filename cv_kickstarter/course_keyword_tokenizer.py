"""Extract raw keywords from course.

course_keyword_tokenizer extracts raw keyword tokens from courses with
noun phrase chunking.
"""
import nltk
from cv_kickstarter import nltk_data_downloader

nltk_data_downloader.download()


def course_keyword_tokens(course):
    """Return keyword tokens for course."""
    return CourseKeywordTokenizer(course).keyword_tokens()


class CourseKeywordTokenizer(object):

    """Can extract keyword tokens from course."""

    def __init__(self, course):
        """Initialize with course."""
        self.course = course

    def keyword_tokens(self):
        """Return keyword tokens for course."""
        if self.course is None:
            return []
        return [token for sentence in self._course_sentences()
                for token in TextKeywordChunkifier().chunks(sentence)]

    def _course_sentences(self):
        return CourseSentenceExtractor(self.course).sentences()


class CourseSentenceExtractor(object):

    """Can extact sentences from course object."""

    def __init__(self, course):
        """Initialize with course."""
        self.course = course

    def sentences(self):
        """Return sentences for course.

        The sentences are based on title, contents, course_objectives_text
        and course_objectives
        """
        return [sentence for text in self._course_texts() if text is not None
                for sentence in nltk.sent_tokenize(text)]

    def _course_texts(self):
        return [
            self.course.title,
            self.course.contents,
            self.course.course_objectives_text
        ] + list(self.course.course_objectives)


class TextKeywordChunkifier(object):

    """Can split text into several chunks by noun phrase chunking.

    The chunks are extracted with noun phrase chunking with nouns and preceding
    adjectives (if there are any).

    The code in this class is inspired by the NLTK book and Finn Nielsens
    code from Data Mining using Python 02819 from DTU.
    """

    def chunks(self, text):
        """Return keyword chunks from the given text."""
        return self._extract_chunks(
            self._grammar_parser().parse(
                nltk.pos_tag(nltk.word_tokenize(text))
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
