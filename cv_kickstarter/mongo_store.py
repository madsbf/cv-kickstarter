from werkzeug import cached_property
from pymongo import Connection


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
        return self._connection.db[self._database_name]

    @cached_property
    def _connection(self):
        if self.mongo_db_url:
            return Connection(self.mongo_db_url)
        else:
            return Connection('localhost', 27017)
