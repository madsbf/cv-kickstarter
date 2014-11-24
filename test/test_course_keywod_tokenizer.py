from cv_kickstarter.course_keyword_tokenizer import (
    CourseSentenceExtractor, TextChunkifier
)
from mock import MagicMock


def test_extraction_of_sentences_from_course():
    course = MagicMock(
        title='02819 Data Mining using Python',
        contents='The course starts with lectures that introduce the Python '
                 + 'programming language. In the last part of the course '
                 + 'the participants make a programming project.',
        course_objectives_text='To give the participants knowledge about '
                               + 'Python programming.',
        course_objectives=[
            "Design an application",
            "Implement an application in Python",
            "Implement code testing in Python for an application in Python",
        ]
    )
    assert CourseSentenceExtractor(course).sentences() == [
        '02819 Data Mining using Python',
        'The course starts with lectures that introduce the Python ' +
        'programming language.',
        'In the last part of the course the participants make a '
        + 'programming project.',
        'To give the participants knowledge about Python programming.',
        "Design an application",
        "Implement an application in Python",
        "Implement code testing in Python for an application in Python"
    ]


def assert_chunkification(text, chunks):
    assert TextChunkifier().text_chunks(text) == chunks


def test_sane_chunks_from_course_goals():
    assert_chunkification(
        "Design an application",
        ["design", "application"]
    )
    assert_chunkification(
        "Implement an application in Python",
        ["implement", "application", "python"]
    )
    assert_chunkification(
        "Implement code testing in Python for an application in Python",
        ["implement code testing", "python", "application", "python"]
    )
    # Would be nice with "text processing" instead of "processing" here
    assert_chunkification(
        "Apply numerical, computational, statistical or machine learning "
        + "parts of Python or methods to text processing",
        ["machine learning parts", "python", "methods", "processing"]
    )
    assert_chunkification(
        "Choose between different methods for gathering, processing and "
        + "presenting data through Python",
        ["choose", "different methods", "processing", "data", "python"]
    )
    assert_chunkification(
        "Apply structured documentation in Python",
        ["documentation", "python"]
    )
    assert_chunkification(
        "Explain and report work throught a technical document",
        ["explain", "report work throught", "technical document"]
    )
