"""Course Repository for storing and fetching courses from MongoDB."""
from collections import namedtuple
from werkzeug import cached_property
from pymongo import Connection


class CourseRepository(object):

    """Stores and fetches course objects.

    CourseRepository is able to fetch course data and deserialize to course
    objects and store given course objects by serializing to JSON and
    store in MongoDB through the mongo_store.
    """

    def __init__(self, mongo_store, collection='courses'):
        """Initialize with mongo_store and optional collection.

        The mongo_store need to be able to perform insert, remove and find.
        """
        self.mongo_store = mongo_store
        self.collection = collection

    def create(self, course, tokens):
        """Create course with tokens in MongoDB by serializing into JSON."""
        self.mongo_store.insert(self.collection, {
            "course_number": course.course_number,
            "title": course.title,
            "contents": course.contents,
            "course_objectives_text": course.course_objectives_text,
            "course_objectives": course.course_objectives,
            "tokens": tokens
        })

    def remove(self, course_number):
        """Remove course with given course_number from MongoDB."""
        self.mongo_store.remove(
            self.collection,
            {"course_number": course_number}
        )

    def find_by_course_number(self, course_number):
        """Find course by given course number in MongoDB."""
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

    """Database Client for MongoDB."""

    def __init__(self, database_name, mongo_db_url=None):
        """Initialize with database_name and optional mongo_db_url.

        If mongo_db_url is not given the database connection defaults to
        using localhost.
        """
        self._database_name = database_name
        self.mongo_db_url = mongo_db_url

    def insert(self, collection, hash_data):
        """Insert hash_data (document) into collection."""
        self._collection(collection).insert(hash_data)

    def find(self, collection, query):
        """Find document in collection by query."""
        return self._collection(collection).find_one(query)

    def remove(self, collection, query):
        """Remove document in collection by query."""
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
