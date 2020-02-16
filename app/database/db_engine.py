from enum import Enum
from datetime import datetime

import tzlocal
import pytz
import pymongo
from bson import objectid, CodecOptions


class DBEngine:
    def __init__(self, db_url, db_name, collection_name):
        self.db_url = db_url
        self.db_name = db_name
        self.collection_name = collection_name

        self.client = pymongo.MongoClient(self.db_url)
        self.db = self.client[self.db_name]        
        self.collection = self.db[collection_name]

        codec_options = CodecOptions(tz_aware=True, tzinfo=tzlocal.get_localzone())
        self.collection = self.collection.with_options(codec_options=codec_options)

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
            upload_date_with_timezone = upload_date.replace(tzinfo=pytz.UTC)
            local_upload_date = upload_date_with_timezone.astimezone(tzlocal.get_localzone())
            file_name = local_upload_date.strftime('%d-%m-%Y_%H-%M-%S_tmp.py')

        if tags is None or (len(tags) == 1 and tags[0] == ''):
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


    @classmethod
    def convert_to_id(cls, value):
        if not cls.is_valid_id(value):
            raise ValueError(f'invalid ObjectId(={value})')
        else:
            return objectid.ObjectId(value)

    
    @staticmethod
    def generate_id():
        return objectid.ObjectId()


    def upload(self, file_name, code, tags):
        serialized_file = self.serialize_file(file_name, code, tags)

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
            '_id': id
        })


class StorageType(Enum):
    TEMPORARY = 'tmp'
    DATABASE = 'db'


class DBViewType(Enum):
    ALL = 'all'
    ANY_TAG_MATCH = 'any_match'
    ALL_TAGS_MATCH = 'full_match'
