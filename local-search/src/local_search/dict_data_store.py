import abc
from typing import List, Dict
from src.local_search.KeyValuePair import KeyValuePair
import json


class DictDataStore(metaclass=abc.ABCMeta):
    def __init__(self):
        self.data = {}

    def put(self, entity: str, key: str, value: any):
        if entity not in self.data:
            self.data[entity] = {}
        self.data[entity][key] = value

    def put_if_not_exists(self, entity: str, key: str, value: str):
        if not entity in self.data:
            self.data[entity] = {}

        if not key in self.data[entity]:
            self.data[entity][key] = value

    def get(self, entity: str, key: str) -> any:
        if entity not in self.data:
            return None
        if key not in self.data[entity]:
            return None
        return self.data[entity][key]

    def put_bulk(self, entity: str, key_value_pairs: List[KeyValuePair]):
        pass

    def get_bulk(self, entity: str, keys: List[str]):
        pass

    def show_db(self):
        print(str(self.data).replace("], ", "],\n"))

    def export_to_file(self, file_path: str):
        self._to_json(self.data, file_path)

    def import_from_file(self, file_path: str):
        self.data = self._from_json(file_path)

    def _to_json(self, data: Dict, file_path: str):
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def _from_json(self, file_path: str):
        with open(file_path, 'r') as file:
            data_str = file.read()
        return json.loads(data_str)


