from datetime import datetime

from bson.objectid import ObjectId
import pymongo


class DBEngine:
    def __init__(self, mongo_url, db_name, collection_name):
        self.mongo_url = mongo_url
        self.db_name = db_name

        self.mongo = pymongo.MongoClient(self.mongo_url) # MongoDB instance
        self.db = self.mongo[self.db_name]               # Database
        self.collection = self.db[collection_name]       # Collection

        self.collection.create_index('file_name')
        self.collection.create_index('upload_date')
        self.collection.create_index([
            ('file_name', pymongo.ASCENDING),
            ('upload_date', pymongo.DESCENDING)
        ])
      
    
    def upload(self, file_name, code, tags):
        insert_result = self.collection.insert_one({
            'file_name': file_name,
            'code': code,
            'tags': tags,
            'length': len(code),
            'upload_date': datetime.utcnow()
        })

        return insert_result.inserted_id


    def get_tags(self):
        return self.collection.distinct('tags')


    def get_files_by_any_tags(self, tags):
        return self.collection.find({
            'tags': {
                '$elemMatch': {
                    '$in': tags
                }
            }
        })


    def get_files_by_tags(self, tags):
        return self.collection.find({
            'tags': {
                '$all': tags
            }
        })


    def get_file_by_id(self, id):
        return self.collection.find_one({
            '_id': ObjectId(id)
        })
