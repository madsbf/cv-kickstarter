class CourseBaseRepo(object):
    def __init__(self, courses):
        self.courses = courses
        self.indexed_courses = {}
        for course in self.courses:
            self.indexed_courses[course.course_number] = course

    def find_by_course_number(self, course_number):
        try:
            return self.indexed_courses[course_number]
        except KeyError:
            return None
