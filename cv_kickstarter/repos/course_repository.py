import sys
sys.path.append("cv_kickstarter/models")
from course import Course


class CourseRepository(object):
    def __init__(self, mongo_store, collection='dtu_student_cvs'):
        self.mongo_store = mongo_store
        self.collection = collection

    def create(self, course, tokens):
        self.mongo_store.insert(self.collection, {
            "course_number": course.course_number,
            "title": course.title,
            "contents": course.contents,
            "course_objectives_text": course.course_objectives_text,
            "course_objectives": course.course_objectives,
            "tokens": tokens
        })

    def remove(self, course_number):
        self.mongo_store.remove(
            self.collection,
            {"course_number": course_number}
        )

    def find_by_course_number(self, course_number):
        return self._map_to_course(self.mongo_store.find(
            self.collection,
            {"course_number": course_number}
        ))

    def _map_to_course(self, mongo_course):
        if not mongo_course:
            return None
        return Course(
            mongo_course['title'],
            mongo_course['course_number'],
            mongo_course['contents'],
            mongo_course['course_objectives_text'],
            mongo_course['course_objectives'],
            mongo_course['tokens']
        )
