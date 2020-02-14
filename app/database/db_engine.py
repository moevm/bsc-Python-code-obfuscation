from datetime import datetime

import pymongo
from bson import objectid


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


    @staticmethod
    def serialize_file(file_name, code, tags):
        upload_date = datetime.utcnow()

        if file_name is None:
            file_name = upload_date.strftime('%d-%m-%Y_%H-%M-%S_tmp.py')

        if tags is None:
            tags =[]

        return {
            'file_name': file_name,
            'code': code,
            'tags': tags,
            'length': len(code),
            'upload_date': upload_date
        }


    @staticmethod    
    def is_valid_id(id):
        return objectid.ObjectId.is_valid(id)


    def upload(self, file_name, code, tags):
        serialized_file = DBEngine.serialize_file(file_name, code, tags)

        insert_result = self.collection.insert_one(serialized_file)

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
