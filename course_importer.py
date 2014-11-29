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
        print("importing course %s/%s" % (index, course_size))
        course_repo.remove(course.course_number)
        course_repo.create(
            course,
            course_keyword_tokenizer.course_tokens(course)
        )
        index = index + 1

if __name__ == '__main__':
    import_courses()
