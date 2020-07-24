import abc
from typing import List
from src.local_search.KeyValuePair import KeyValuePair
import json


class DictDataStore(metaclass=abc.ABCMeta):
    def __init__(self):
        self.data = {}

    def put(self, key: str, value: any):
        self.data[key] = value

    def get(self, key: str) -> any:
        if key not in self.data:
            return None
        return self.data[key]

    def put_bulk(self, key_value_pairs: List[KeyValuePair]):
        pass

    def get_bulk(self, keys: List[str]):
        pass

    def show_db(self):
        print(str(self.data).replace("], ", "],\n"))

    def export_to_file(self, file_path):
        self._to_json(file_path)

    def import_from_file(self, file_path):
        self._from_json(file_path)

    def _to_json(self, file_path: str):
        with open(file_path, 'w') as file:
            json.dump(self.data, file)

    def _from_json(self, file_path: str):
        with open(file_path, 'r') as file:
            data_str = file.read()
        self.data = json.loads(data_str)
