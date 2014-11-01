class GradeAverageCalculator(object):
    def __init__(self, exam_results):
        self.exam_results = exam_results

    def average_grade(self):
        return round(self._raw_average_grade(), 1)

    def _raw_average_grade(self):
        return (self._sum_of_products_of_grade_and_ects() /
                self._total_ects_points())

    def _sum_of_products_of_grade_and_ects(self):
        return sum(
            map(
                self._product_of_grade_and_ects,
                self._exam_results_with_grade()
            )
        )

    def _total_ects_points(self):
        return sum(self._ects_points_of_exam_results_with_grade())

    def _product_of_grade_and_ects(self, exam_result):
        return exam_result.grade * exam_result.ects_points

    def _ects_points_of_exam_results_with_grade(self):
        return map(lambda x: x.ects_points, self._exam_results_with_grade())

    def _exam_results_with_grade(self):
        return filter(self._is_result_with_grade, self.exam_results)

    def _is_result_with_grade(self, exam_result):
        return isinstance(exam_result.grade, int)
