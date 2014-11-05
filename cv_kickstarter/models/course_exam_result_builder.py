from exam_result import ExamResult


class CourseExamResultBuilder(object):
    def __init__(self, exam_result, course_base):
        self.exam_result = exam_result
        self.course_base = course_base

    def course_exam_result(self):
        return ExamResult(
            self.exam_result.grade,
            self._course_from_course_base(self.exam_result.course_number)
        )

    def _course_from_course_base(self, course_number):
        return self.course_base.find_by_course_number(course_number)
