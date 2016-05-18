"""
Contains the MongoInterface class as part of the db subpackage.
"""
import pymongo
from talata_bont_backend.util import log


log.init_logger()
logger = log.get_logger()


class MongoInterface:

    """
    Creates necessary functions to interact with mongodb.
    """

    def __init__(self, host, port, db_name):
        """
        Init mongo cliend and db.

        Args:
            host (str): host name or IP [machine specific]
            port (str)
            db_name (str)
        """
        self._client = pymongo.MongoClient(host, port)
        self._db = self._client[db_name]

    def insert_one(self, collection_name, item):
        """
        Insert one item into the passed collection.

        Args:
            collection_name (str): name of mongo collection [table]
            item (dict): item to insert
        """
        collection = self._db[collection_name]
        collection.insert_one(item)

    def insert_many(self, collection_name, items):
        """
        Insert multiple items into the passed collection.

        Args:
            collection_name (str): name of mongo collection [table]
            item (dict): item to insert
        """
        collection = self._db[collection_name]
        collection.insert_many(items)

    def find(self, collection_name, filters, by_date=None):
        """
        Find documents in the db given some filters.

        Args:
            collection_name (str): name of mongo collection [table]
            filters (dict)
            sorting_attribute (str): attribute used for sorting
        """
        collection = self._db[collection_name]

        if by_date:
            return collection.find(filters).sort('date',
                                                 pymongo.DESCENDING)
        else:
            return collection.find(filters)

    def count(self, collection_name):
        """
        Get count of documents in a collection.

        Args:
            collection_name (str)

        Returns:
            int: count
        """
        return self._db[collection_name].count()
