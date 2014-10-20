import xml.etree.ElementTree as xmlET


def courses_from_xml(courses_xml_text):
    courses = xmlET.fromstring(courses_xml_text).findall(
        'Courses/FullXML/Course'
    )
    return [CourseExtractor(course).course() for course in courses]


class CourseExtractor(object):
    def __init__(self, course_xml):
        self.course_xml = course_xml

    def course(self):
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
        return self.course_xml.find("Title[@Lang='da-DK']").attrib['Title']

    def _contents(self):
        return self.course_xml.find("Txt[@Lang='da-DK']/Contents").text

    def _course_objectives_text(self):
        return self.course_xml.find(
            "Txt[@Lang='da-DK']/Course_Objectives"
        ).text

    def _course_objectives(self):
        return [objective_xml.attrib['Txt']
                for objective_xml in self._course_objectives_xml()]

    def _course_objectives_xml(self):
        return self.course_xml.findall(
            "DTU_ObjectiveKeyword/Txt[@Lang='da-DK']"
        )


class Course(object):
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
