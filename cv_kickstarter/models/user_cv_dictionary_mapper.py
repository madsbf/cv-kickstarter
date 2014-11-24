class UserCVDictionaryMapper(object):
    def user_cv_dict(self, user_cv, student_number):
        return {
            "student_number": student_number,
            "first_name": user_cv.first_name,
            "last_name": user_cv.last_name,
            "exam_result_programmes": list(map(
                self._map_exam_result_programme,
                user_cv.exam_result_programmes
            )),
            "keywords": list(map(
                self._map_keyword,
                user_cv.keywords
            ))
        }

    def _map_exam_result_programme(self, exam_result_programme):
        return {
            "name": exam_result_programme.name,
            "passed_ects": exam_result_programme.passed_ects,
            "total_ects": exam_result_programme.total_ects,
            "exam_results": list(map(
                self._exam_result,
                exam_result_programme.exam_results
            ))
        }

    def _exam_result(self, exam_result):
        return {
            "grade": exam_result.grade,
            "course_title": exam_result.course_title,
            "course_number": exam_result.course_number,
            "ects_points": exam_result.ects_points
        }

    def _map_keyword(self, keyword):
        return {
            "keyword": keyword.keyword,
            "rank": keyword.rank,
            "courses": list(map(self._map_course, keyword.course_numbers))
        }

    def _map_course(self, course):
        return {
            "title": course.title,
            "course_number": course.course_number
        }
