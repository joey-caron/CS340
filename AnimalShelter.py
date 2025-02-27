from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, USER, PASS, HOST, PORT, DB, COL):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

# method to implement the C in CRUD.
    def create(self, data):
        if data:
            result = self.collection.insert_one(data)  # data should be dictionary         
            if result.inserted_id is None: # check inserted id result to verify if creation was successful or not
                return False
            return True # default
        else:
            raise Exception("Nothing to save, because info parameter is empty")

# method to implement the R in CRUD.
    def read(self, data):
        results = self.collection.find(data) # data can be any key, value combination in dictionary
        return list(results) #Returns a list of dictionaries instead of a string
        
            
# method to implement the U in CRUD.
    def update(self, data, udata):
        if data:
            if self.collection.count_documents(data) == 1: #separate loops for update_one and update_many
                if udata is not None:
                    updated = self.collection.update_one(data, {'$set': udata}) #data is search key, udata is info to be updated
                else:
                    raise Exception("No information to update provided.")
            elif self.collection.count_documents(data) >= 2:
                if udata is not None:
                    updated = self.collection.update_many(data, {'$set': udata})
                else:
                    raise Exception("No information to update provided.")
            else:
                raise Exception("No documents found with provided search parameters.")                        
            return updated.modified_count
        else:
            raise Exception("Must enter key: value combination to find document to update")
            
# method to implement the D in CRUD
    def delete(self, data):
        if data:
            if self.collection.count_documents(data) == 1: #separate loops for delete_one and delete_many
                deleted = self.collection.delete_one(data) # data any key: value combination as dictionary
            elif self.collection.count_documents(data) >= 2:
                deleted = self.collection.delete_many(data)
            else:
                raise Exception("No documents found, nothing deleted")
            return deleted.deleted_count
        else:
            raise Exception("Must enter key: value combination to find document to delete")
