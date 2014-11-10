import sys

sys.path.append('dtu_course_base')

from course_base_repo import CourseBaseRepo
import dtu_course_base


class XmlCourseBaseRepoBuilder(object):
    def __init__(self, course_xml_path):
        self.course_xml_path = course_xml_path

    def course_base_repo(self):
        return CourseBaseRepo(self._courses_from_xml())

    def _courses_from_xml(self):
        return dtu_course_base.courses_from_xml(self._course_xml())

    def _course_xml(self):
        return open('courses.xml').read()
