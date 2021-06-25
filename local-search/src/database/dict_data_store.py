import abc
from typing import List, Dict
from database.KeyValuePair import KeyValuePair
import json


class DictDataStore(metaclass=abc.ABCMeta):
    def __init__(self):
        self.data = {}

    def clear(self):
        self.data = {}

    def put(self, entity: str, key: str, value: any):
        if entity not in self.data:
            self.data[entity] = {}
        self.data[entity][key.encode()] = self.encode_value(value)

    def put_if_not_exists(self, entity: str, key: str, value: str):

        if not entity in self.data:
            self.data[entity] = {}
        encoded_key = key.encode()

        if not encoded_key in self.data[entity]:
            self.data[entity][encoded_key] = self.encode_value(value)

    def decode_value(self, value):
        if type(value) == list:
            return [element.decode() for element in value]
        else:
            return value.encode()

    def encode_value(self, value):
        if type(value) == list:
            return [element.encode() for element in value]
        else:
            return value.encode()

    def get(self, entity: str, key: str) -> any:
        if entity not in self.data:
            return None

        encoded_key = key.encode()

        if encoded_key not in self.data[entity]:
            return None

        return self.decode_value(self.data[entity][encoded_key])

    def get_all_keys(self, entity: str) -> List[str]:
        if not entity in self.data:
            return []

        return [key.decode() for key in self.data[entity].keys()]

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
            data_str = ""
            line = " "
            while(line):
                data_str += line
                line = file.readline()

        return json.loads(data_str)


