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
        MongoStore(config.mongo_db_name(), config.mongo_url())
    )
    progress_bar = ProgressBar(len(courses))
    for index, course in enumerate(courses):
        progress_bar.update(index)
        course_repo.remove(course.course_number)
        course_repo.create(
            course,
            course_keyword_tokenizer.course_tokens(course)
        )


class ProgressBar(object):
    def __init__(self, enumeration_size):
        self.enumeration_size = enumeration_size

    def update(self, index):
        progress = int(index / self.enumeration_size * 100)
        hashes = '=' * progress + '>'
        spaces = '.' * (100 - progress)
        sys.stdout.write(
            "\rImporting courses: [{0}] {1}%, course {2}/{3}".format(
                hashes + spaces,
                progress,
                index,
                self.enumeration_size
            )
        )
        sys.stdout.flush()


if __name__ == '__main__':
    import_courses()
