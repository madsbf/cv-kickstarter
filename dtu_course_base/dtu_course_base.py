"""Python library for structuring courses based on xml response
from the DTU Course Base.
"""

import xml.etree.ElementTree as xmlET


def courses_from_xml(courses_xml_text, language='en-GB'):
    """Extracts course objects based on xml with courses"""
    courses = xmlET.fromstring(courses_xml_text).findall(
        'Courses/FullXML/Course'
    )
    return [CourseExtractor(course, language).course() for course in courses]


class CourseExtractor(object):
    """Class that is able to extract and return course objects based
    on a course xml object.
    """

    def __init__(self, course_xml, language):
        """Construct CourseExtractor based on course xml and a language.

        The language can be either 'en-GB' or 'da-DK' for respectively
        english or danish
        """
        self.course_xml = course_xml
        self.language = language

    def course(self):
        """Returns a Course object with information based on the given
        course xml
        """
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
        return self.course_xml.find(
            "Txt[@Lang='%s']/Contents" % self.language
        ).text

    def _course_objectives_text(self):
        return self.course_xml.find(
            "Txt[@Lang='%s']/Course_Objectives" % self.language
        ).text

    def _course_objectives(self):
        return [objective_xml.attrib['Txt']
                for objective_xml in self._course_objectives_xml()]

    def _course_objectives_xml(self):
        return self.course_xml.findall(
            "DTU_ObjectiveKeyword/Txt[@Lang='%s']" % self.language
        )


class Course(object):
    """Structured class for course info from DTU Course Base"""

    def __init__(
        self,
        title,
        course_number,
        contents,
        course_objectives_text,
        course_objectives
    ):
        self.title = title
        self.course_number = course_number
        self.contents = contents
        self.course_objectives_text = course_objectives_text
        self.course_objectives = course_objectives
