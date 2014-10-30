class UserCVExamResult(object):
    def __init__(self, exam_result):
        self.exam_result = exam_result

    @property
    def course_title(self):
        return self.exam_result.course_title

    @property
    def ects_points(self):
        return self.exam_result.ects_points

    @property
    def grade(self):
        return self.exam_result.grade

    @property
    def url(self):
        return "http://www.kurser.dtu.dk/%s.aspx" % self.course_number

    @property
    def course_number(self):
        return self.exam_result.course_number

    @property
    def programme(self):
        return self.exam_result.programme
