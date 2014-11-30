from collections import namedtuple
from werkzeug import cached_property
from pymongo import Connection


class CourseRepository(object):
    def __init__(self, mongo_store, collection='courses'):
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


class MongoStore(object):
    def __init__(self, database_name, mongo_db_url=None):
        self._database_name = database_name
        self.mongo_db_url = mongo_db_url

    def insert(self, collection, hash_data):
        self._collection(collection).insert(hash_data)

    def find(self, collection, query):
        return self._collection(collection).find_one(query)

    def remove(self, collection, query):
        self._collection(collection).remove(query)

    def _collection(self, collection):
        return self._database[collection]

    @cached_property
    def _database(self):
        return self._connection[self._database_name]

    @cached_property
    def _connection(self):
        if self.mongo_db_url:
            return Connection(self.mongo_db_url)
        else:
            return Connection('localhost', 27017)


Course = namedtuple("Course", ['title', 'course_number', 'contents',
                               'course_objectives_text', 'course_objectives',
                               'tokens'])
