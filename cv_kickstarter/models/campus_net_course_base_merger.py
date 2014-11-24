from functools import reduce


class CampusNetCourseBaseMerger(object):
    def __init__(self, exam_result_programmes, course_base):
        self.exam_result_programmes = exam_result_programmes
        self.course_base = course_base

    def course_exam_results(self):
        return list(map(
            self._map_campus_net_exam_result,
            self._campus_net_exam_results()
        ))

    def _map_campus_net_exam_result(self, exam_result):
        return ExamResult(
            exam_result.grade,
            self.course_base.find_by_course_number(
                exam_result.course_number
            ),
            exam_result.ects_points
        )

    def _campus_net_exam_results(self):
        return reduce(
            lambda x, y: x + y,
            map(
                lambda x: x.exam_results,
                self.exam_result_programmes
            ),
            []
        )


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
