from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoDBInterface:
    def __init__(self, uri: str, database_name: str):
        """
        Initialize the MongoDBInterface with a connection URI and database name.
        """
        self.uri = uri
        self.database_name = database_name
        self.client = None
        self.db = None

    def connect(self):
        """
        Establish a connection to the MongoDB server.
        """
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.database_name]
            # Test connection
            self.client.admin.command('ping')
            print("Connected to MongoDB successfully.")
            return True
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            self.client = None
            self.db = None
        return False

    def disconnect(self):
        """
        Close the connection to the MongoDB server.
        """
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB.")
            self.client = None
            self.db = None

    def insert_one(self, collection_name: str, document: dict):
        """
        Insert a single document into a collection.
        """
        if self.db is None:
            raise ConnectionError("Not connected to MongoDB.")
        return self.db[collection_name].insert_one(document)

    def insert_many(self, collection_name: str, documents: list):
        """
        Insert multiple documents into a collection.
        """
        if self.db is None:
            raise ConnectionError("Not connected to MongoDB.")
        return self.db[collection_name].insert_many(documents)

    def find_one(self, collection_name: str, query: dict, projection: dict = None):
        """
        Find a single document in a collection.
        """
        if self.db is None:
            raise ConnectionError("Not connected to MongoDB.")
        return self.db[collection_name].find_one(query, projection)

    def find_many(self, collection_name: str, query: dict, projection: dict = None, limit: int = 0):
        """
        Find multiple documents in a collection.
        """
        if self.db is None:
            raise ConnectionError("Not connected to MongoDB.")
        cursor = self.db[collection_name].find(query, projection)
        if limit > 0:
            cursor = cursor.limit(limit)
        return list(cursor)

    def update_one(self, collection_name: str, query: dict, update: dict, upsert: bool = False):
        """
        Update a single document in a collection.
        """
        if self.db is None:
            raise ConnectionError("Not connected to MongoDB.")
        return self.db[collection_name].update_one(query, update, upsert=upsert)

    def update_many(self, collection_name: str, query: dict, update: dict, upsert: bool = False):
        """
        Update multiple documents in a collection.
        """
        if self.db is None:
            raise ConnectionError("Not connected to MongoDB.")
        return self.db[collection_name].update_many(query, update, upsert=upsert)

    def delete_one(self, collection_name: str, query: dict):
        """
        Delete a single document from a collection.
        """
        if self.db is None:
            raise ConnectionError("Not connected to MongoDB.")
        return self.db[collection_name].delete_one(query)

    def delete_many(self, collection_name: str, query: dict):
        """
        Delete multiple documents from a collection.
        """
        if self.db is None:
            raise ConnectionError("Not connected to MongoDB.")
        return self.db[collection_name].delete_many(query)

    def count_documents(self, collection_name: str, query: dict):
        """
        Count the number of documents matching a query in a collection.
        """
        if self.db is None:
            raise ConnectionError("Not connected to MongoDB.")
        return self.db[collection_name].count_documents(query)

    def create_index(self, collection_name: str, keys: list, **kwargs):
        """
        Create an index on a collection.
        """
        if self.db is None:
            raise ConnectionError("Not connected to MongoDB.")
        return self.db[collection_name].create_index(keys, **kwargs)

    def list_collections(self):
        """
        List all collections in the database.
        """
        if self.db is None:
            raise ConnectionError("Not connected to MongoDB.")
        return self.db.list_collection_names()
    
    def distinct(self, collection_name: str, field: str, query: dict = None):
        """
        Get distinct values for a specified field in a collection.
        """
        if self.db is None:
            raise ConnectionError("Not connected to MongoDB.")
        return self.db[collection_name].distinct(field, query or {})