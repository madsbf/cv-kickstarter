from collections import namedtuple

FakeTokenizedExamResult = namedtuple(
    'FakeTokenizedExamResult',
    ['exam_result', 'course', 'tokens']
)

FakeExamResult = namedtuple(
    'FakeExamResult',
    ['grade', 'ects_points']
)

FakeCourse = namedtuple('FakeCourse', ['course_number'])
