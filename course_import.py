"""Import courses from the course base into MongoDB.

Because of optimization reasons all courses are imported into MongoDB from
the course xml.

NB: This import is necessary to display course skills and job recommendations.
"""
from __future__ import division
import sys

from cv_kickstarter import dtu_course_base
from cv_kickstarter import course_keyword_tokenizer
from cv_kickstarter.course_repository import CourseRepository, MongoStore
from cv_kickstarter.cv_kickstarter_config import CvKickstarterConfig


def import_courses(course_xml_path='courses.xml'):
    """Import courses from xml into MongoDB to be used by CVKickstarter."""
    courses = dtu_course_base.courses_from_xml(open(course_xml_path).read())
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
            course_keyword_tokenizer.course_keyword_tokens(course)
        )


class ProgressBar(object):

    """For displaying a progress bar with progress of the import."""

    def __init__(self, enumeration_size):
        """Initialize with enumerate_size - the amount of objects iterated."""
        self.enumeration_size = enumeration_size

    def update(self, index):
        """Update the progress bar by the given iteration index."""
        progress = int((index + 1) / self.enumeration_size * 100)
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
