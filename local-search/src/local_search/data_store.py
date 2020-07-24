import abc
from typing import List
from src.local_search.KeyValuePair import KeyValuePair


class DataStore(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def put(self, entity: str, key: str, value: any):
        pass

    @abc.abstractmethod
    def get(self, entity: str, key: str) -> any:
        return None

    @abc.abstractmethod
    def put_bulk(self, entity: str, key_value_pairs: List[KeyValuePair]):
        pass

    @abc.abstractmethod
    def get_bulk(self, entity: str, keys: List[str]):
        pass

    @abc.abstractmethod
    def export_to_file(self, entity: str, file_path: str):
        pass

    @abc.abstractmethod
    def import_from_file(self, entity: str, file_path: str):
        pass
