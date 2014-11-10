def average_grade(exam_results):
    return GradeAverageCalculator(exam_results).average_grade()


class GradeAverageCalculator(object):
    def __init__(self, exam_results):
        self.exam_results = exam_results

    def average_grade(self):
        if not self.exam_results or not self._contains_graded_courses():
            return None
        return round(self._raw_average_grade(), 1)

    def _raw_average_grade(self):
        return (sum(self._products_of_grades_and_ects()) /
                self._total_ects_points())

    def _products_of_grades_and_ects(self):
        return map(
            self._product_of_grade_and_ects,
            self._exam_results_with_grade()
        )

    def _total_ects_points(self):
        return sum(self._ects_points_of_exam_results_with_grade())

    def _contains_graded_courses(self):
        return len(list(self._ects_points_of_exam_results_with_grade())) > 0

    def _product_of_grade_and_ects(self, exam_result):
        return exam_result.grade * exam_result.ects_points

    def _ects_points_of_exam_results_with_grade(self):
        return map(lambda x: x.ects_points, self._exam_results_with_grade())

    def _exam_results_with_grade(self):
        return filter(self._is_result_with_grade, self.exam_results)

    def _is_result_with_grade(self, exam_result):
        return isinstance(exam_result.grade, int)
