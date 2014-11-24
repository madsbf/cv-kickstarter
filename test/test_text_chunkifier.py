import sys
sys.path.append('cv_kickstarter/models')

from course_keyword_tokenizer import TextChunkifier


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
