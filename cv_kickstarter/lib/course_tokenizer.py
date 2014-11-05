from exam_result import ExamResult


class CampusNetCourseBaseMapper(object):
    def __init__(self, campus_net_client, course_base):
        self.campus_net_client = campus_net_client
        self.course_base = course_base

    def course_exam_results(self):
        return list(map(
            self._map_campus_net_exam_result,
            self._campus_net_exam_results()
        ))

    def _map_campus_net_exam_result(self, exam_result):
        return ExamResult(
            exam_result.grade,
            self._course_from_course_base(exam_result.course_number)
        )

    def _course_from_course_base(self, course_number):
        return self.course_base.find_by_course_number(course_number)

    def _campus_net_exam_results(self):
        return reduce(
            lambda x, y: x + y,
            map(lambda x: x.exam_results, self._exam_result_programmes())
        )

    def _exam_result_programmes(self):
        return
