import abc
from typing import List
from src.local_search.KeyValuePair import KeyValuePair


class DataStore(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def put(self, key: str, value: any):
        pass

    @abc.abstractmethod
    def get(self, key: str) -> any:
        return None

    @abc.abstractmethod
    def put_bulk(self, key_value_pairs: List[KeyValuePair]):
        pass

    @abc.abstractmethod
    def get_bulk(self, keys: List[str]):
        pass

