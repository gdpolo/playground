import abc
from typing import List, Dict

from pymongo.collection import Collection
from pymongo.database import Database

from database.KeyValuePair import KeyValuePair
import json

from database.data_store import DataStore

from pymongo import MongoClient, ASCENDING, UpdateOne, ReplaceOne


class MongoDataStore(DataStore):
    def __init__(self, entities: List[str]):
        super().__init__()

        # todo - move parameters to config
        self.client = MongoClient('localhost', 27017,
                                  username='gilda',
                                  password='123456',
                                  authSource='local_search_data')

        self.db: Database = self.client.local_search_data

        for entity in entities:
            #self.collections = {entity: self.db[entity] for entity in entities}
            self.db[entity].create_index([('key', ASCENDING)], unique=True)

    def clear(self):
        # todo - hard coded
        existing_collections = self.db.list_collection_names()
        for collection_name in ['words', 'files']:
            if collection_name in existing_collections:
               self.db['collection_name'].drop()

    def put(self, entity: str, key: str, value: any):
        collection: Collection = self.db[entity]
        data = {
            "key": key, #key.encode()
            "value": value
        }
        collection.update_one({"key": key}, data, upsert=True)

    # todo - this should be more generic, should get document or check every field in value
    def bulk_write(self, entity, data: List[KeyValuePair]):
        if not data:
            return

        requests = []
        for kvp in data:
            if type(kvp.value) == list:
                document = {
                    "$set": {"key": kvp.key},
                    "$addToSet": {'value': kvp.value[0]}
                }
            else:
                document = {"$set": {"key": kvp.key, "value": kvp.value}}

            requests.append(UpdateOne({"key": kvp.key}, document, upsert=True))

        self.db[entity].bulk_write(requests, ordered=True)

    def put_if_not_exists(self, entity: str, key: str, value: str):
        collection: Collection = self.db[entity]
        if collection.find_one({"key": key}): #key.encode()
            return
        self.put(entity, key, value)

    def get(self, entity: str, key: str) -> any:
        if entity not in self.db.list_collection_names():
            return None

        collection: Collection = self.db[entity]
        record = collection.find_one({"key": key}) #key.encode()

        if not record:
            return None

        return record['value']  #self.decode_value

    def get_all_keys(self, entity: str) -> List[str]:
        if not entity in self.db:
            return []

        collection: Collection = self.db[entity]
        return [record['key'] for record in collection.find({})]

    def put_bulk(self, entity: str, key_value_pairs: List[KeyValuePair]):
        pass

    def get_bulk(self, entity: str, keys: List[str]):
        pass

    def show_db(self):
        for collection in self.db.list_collections():
            for record in collection.find({}):
                print(str(record))

    # todo - make json directly?
    def export_to_file(self, file_path: str):
        data = {}
        for collection in self.db.list_collections():
            data[collection.name] = {}

            for record in collection.find({}):
                data[collection.name][record['key'], record['value']]


        self._to_json(data, file_path)

    # todo - make json directly?
    def import_from_file(self, file_path: str):
        data = self._from_json(file_path)

        for entity in data:
            for key, record in entity.items():
                self.put(entity, key, record['value'])

    def _to_json(self, data: Dict, file_path: str):
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def _from_json(self, file_path: str):
        with open(file_path, 'r') as file:
            data_str = ""
            line = " "
            while(line):
                data_str += line
                line = file.readline()

        return json.loads(data_str)


