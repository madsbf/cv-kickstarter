from test_fakes import FakeTokenizedExamResult, FakeExamResult, FakeCourse
import academic_skill_set

tokenized_exam_results = [
    FakeTokenizedExamResult(
        FakeExamResult(12, 5.0),
        FakeCourse('02819'),
        ['python', 'python programming', 'data mining', 'machine learning',
         'python']
    ),
    FakeTokenizedExamResult(
        FakeExamResult(7, 10.0),
        FakeCourse('02450'),
        ['machine learning', 'classification', 'python', 'matlab',
         'regression', 'machine learning', 'modelling']
    )
]


def test_skills_from_sentences():
    skill_set = academic_skill_set.skill_set(tokenized_exam_results)
    assert_skill_keywords_in_order(
        skill_set,
        ['machine learning', 'python', 'python programming', 'data mining',
         'classification', 'matlab', 'modelling', 'regression']
    )


def assert_skill_keywords_in_order(actual_skill_set, expected_keywords):
    assert expected_keywords == map(lambda x: x.keyword, actual_skill_set)
