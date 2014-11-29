from __future__ import division
import sys

from cv_kickstarter import dtu_course_base
from cv_kickstarter import course_keyword_tokenizer
from cv_kickstarter.course_repository import CourseRepository
from cv_kickstarter.mongo_store import MongoStore
from cv_kickstarter.cv_kickstarter_config import CvKickstarterConfig


def import_courses():
    courses = dtu_course_base.courses_from_xml(open('courses.xml').read())
    config = CvKickstarterConfig()
    course_repo = CourseRepository(
        MongoStore('cv_kickstarter', config.mongo_url())
    )
    index = 1
    course_size = len(courses)
    for course in courses:
        update_progress(index, course_size)
        course_repo.remove(course.course_number)
        course_repo.create(
            course,
            course_keyword_tokenizer.course_tokens(course)
        )
        index = index + 1


def update_progress(index, course_size):
    progress = int(index / course_size * 100)
    hashes = '=' * progress + '>'
    spaces = '.' * (100 - progress)
    sys.stdout.write(
        "\rImporting courses: [{0}] {1}%, course {2}/{3}".format(
            hashes + spaces,
            progress,
            index,
            course_size
        )
    )
    sys.stdout.flush()

if __name__ == '__main__':
    import_courses()
