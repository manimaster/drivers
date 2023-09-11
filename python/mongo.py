import os
from pymongo import MongoClient

class MongoDB:
    def __init__(self):
        # Get MongoDB connection details from ENV variables
        self.host = os.getenv("MONGO_HOST", "localhost")
        self.port = int(os.getenv("MONGO_PORT", 27017))
        self.username = os.getenv("MONGO_USER", None)
        self.password = os.getenv("MONGO_PASS", None)
        
        self.client = self._connect()
        
    def _connect(self):
        # Establish a connection to the MongoDB server
        if self.username and self.password:
            client = MongoClient(self.host, self.port, username=self.username, password=self.password)
        else:
            client = MongoClient(self.host, self.port)
        return client
    
    def get_database(self, db_name):
        # Return the specified database
        return self.client[db_name]
    
    def list_databases(self):
        # List all the databases
        return self.client.list_database_names()
    
    def create_database(self, db_name):
        # MongoDB creates a database implicitly once data is inserted
        self.client[db_name].new_collection.insert_one({"created": "just to create database"})
        self.client[db_name].new_collection.drop()
    
    def delete_database(self, db_name):
        self.client.drop_database(db_name)
    
    def list_collections(self, db_name):
        return self.client[db_name].list_collection_names()
    
    def create_collection(self, db_name, collection_name):
        self.client[db_name].create_collection(collection_name)
    
    def delete_collection(self, db_name, collection_name):
        self.client[db_name].drop_collection(collection_name)
    
    def insert_document(self, db_name, collection_name, document):
        self.client[db_name][collection_name].insert_one(document)
    
    def find_document(self, db_name, collection_name, query):
        return list(self.client[db_name][collection_name].find(query))
    
    def update_document(self, db_name, collection_name, query, new_values):
        self.client[db_name][collection_name].update_one(query, {"$set": new_values})
    
    def delete_document(self, db_name, collection_name, query):
        self.client[db_name][collection_name].delete_one(query)
    
    def search_documents(self, db_name, collection_name, **kwargs):
        # Flexible search functionality using keyword arguments
        query = {}
        for key, value in kwargs.items():
            query[key] = value
        return self.find_document(db_name, collection_name, query)



# import os

# os.environ["MONGO_HOST"] = "localhost"
# os.environ["MONGO_PORT"] = "27017"


# db = MongoDB()
# db.create_database("testDB")
# db.create_collection("testDB", "testCollection")
# db.insert_document("testDB", "testCollection", {"name": "John", "age": 30})
# db.insert_document("testDB", "testCollection", {"name": "Jane", "age": 25})

# # Search for documents where name is "John"
# print(db.search_documents("testDB", "testCollection", name="John"))

# # Search for documents where age is 30
# print(db.search_documents("testDB", "testCollection", age=30))
