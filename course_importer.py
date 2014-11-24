import sys

sys.path.append("dtu_course_base")
sys.path.append("cv_kickstarter/lib")
sys.path.append("cv_kickstarter/repos")

import dtu_course_base
import course_keyword_tokenizer
from course_repository import CourseRepository
from mongo_store import MongoStore


def import_courses():
    courses = dtu_course_base.courses_from_xml(open('courses.xml').read())
    course_repo = CourseRepository(MongoStore('cv_kickstarter'))
    index = 1
    course_size = len(courses)
    for course in courses:
        print("importing course %s/%s" % (index, course_size))
        course_repo.remove(course.course_number)
        course_repo.create(
            course,
            course_keyword_tokenizer.course_tokens(course)
        )
        index = index + 1
