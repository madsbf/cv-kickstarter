from user_cv_exam_result_programme import UserCVExamResultProgramme


class UserCV(object):
    def __init__(self, first_name, last_name, programme_exam_results):
        self.first_name = first_name
        self.last_name = last_name
        self._programme_exam_results = programme_exam_results

    @property
    def full_name(self):
        return " ".join([self.first_name, self.last_name])

    @property
    def programme_exam_results(self):
        return map(UserCVExamResultProgramme, self._programme_exam_results)
