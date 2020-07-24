import abc
from typing import List
from src.local_search.KeyValuePair import KeyValuePair


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
