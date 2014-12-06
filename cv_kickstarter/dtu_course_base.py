"""Structuring courses based on xml response from the DTU Course Base."""

import xml.etree.ElementTree as xmlET
from collections import namedtuple


def courses_from_xml(courses_xml_text, language='en-GB'):
    """Extract course objects based on xml with courses."""
    courses = xmlET.fromstring(courses_xml_text).findall(
        'Courses/FullXML/Course'
    )
    return [CourseExtractor(course, language).course() for course in courses]


class CourseExtractor(object):

    """Responsible for extracting course objects based on a course xml."""

    def __init__(self, course_xml, language):
        """Construct CourseExtractor based on course xml and a language.

        The language can be either 'en-GB' or 'da-DK' for respectively
        english or danish
        """
        self.course_xml = course_xml
        self.language = language

    def course(self):
        """Return a Course object based on the given course xml."""
        return Course(
            self._title(),
            self._course_number(),
            self._contents(),
            self._course_objectives_text(),
            self._course_objectives()
        )

    def _course_number(self):
        return self.course_xml.attrib['CourseCode']

    def _title(self):
        return self.course_xml.find(
            "Title[@Lang='%s']" % self.language
        ).attrib['Title']

    def _contents(self):
        xml = self.course_xml.find(
            "Txt[@Lang='%s']/Contents" % self.language
        )
        if xml is not None:
            return xml.text

    def _course_objectives_text(self):
        xml = self.course_xml.find(
            "Txt[@Lang='%s']/Course_Objectives" % self.language
        )
        if xml is not None:
            return xml.text

    def _course_objectives(self):
        return [objective_xml.attrib['Txt']
                for objective_xml in self._course_objectives_xml()]

    def _course_objectives_xml(self):
        return self.course_xml.findall(
            "DTU_ObjectiveKeyword/Txt[@Lang='%s']" % self.language
        )


Course = namedtuple("Course", ['title', 'course_number', 'contents',
                               'course_objectives_text', 'course_objectives'])
