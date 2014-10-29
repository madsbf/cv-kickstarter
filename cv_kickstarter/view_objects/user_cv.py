from werkzeug import cached_property
import re


class UserCVBuilder(object):

    def __init__(self, campus_net_client):
        self.campus_net_client = campus_net_client

    def build(self):
        return UserCV(
            self.user.first_name,
            self.user.last_name,
            self.grades
        )

    @cached_property
    def user(self):
        return self.campus_net_client.user()

    @cached_property
    def grades(self):
        return self.campus_net_client.grades()


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


class UserCVExamResultProgramme(object):
    def __init__(self, programme):
        self.programme = programme

    @property
    def name(self):
        return self.programme.name

    @property
    def exam_results(self):
        return map(UserCVExamResult, self.programme.exam_results)

    @property
    def is_done(self):
        if re.search(r"Bachelor", self.programme.name):
            return self._has_passed(180.0)
        elif re.search(r"Master", self.programme.name):
            return self._has_passed(120.0)

    def _has_passed(self, ects_points):
        return self.programme.passed_ects_points >= ects_points


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
