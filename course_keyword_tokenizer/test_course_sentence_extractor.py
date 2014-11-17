import sys
sys.path.append('cv_kickstarter/models')

from course_keyword_tokenizer import CourseSentenceExtractor
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
    print(CourseSentenceExtractor(course).sentences())
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
