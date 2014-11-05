from course_exam_result_builder import CourseExamResultBuilder


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
        return CourseExamResultBuilder(
            exam_result,
            self.course_base
        ).course_exam_result()

    def _campus_net_exam_results(self):
        return reduce(
            lambda x, y: x + y,
            map(
                lambda x: x.exam_results,
                self.exam_result_programmes
            )
        )
