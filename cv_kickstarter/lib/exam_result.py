class ExamResult(object):
    def __init__(self, grade, course, ects_points):
        self.grade = grade
        self.course = course
        self.ects_points = ects_points

    @property
    def course_tokens(self):
        if self.course is None:
            return []
        return self.course.tokens
