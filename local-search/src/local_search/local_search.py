from os.path import basename
from os import walk
from os.path import sep, splitext, join
from typing import List

from src.local_search.dict_data_store import DictDataStore

# TODO - ignore directories or files


class LocalSearch:
    def __init__(self):
        self._data_store = DictDataStore()

    def index_directory(self, root_dir: str):
        # Index current directoy
        for directory, subdir_list, file_list in walk(root_dir):
            words = list(directory.split(sep))

            for file_name in file_list:
                file_name_without_extension = splitext(file_name)[0]
                file_path = join(directory, file_name)
                self._put_data(words + [file_name_without_extension], file_path)

            for sub_directory in subdir_list:
                self.index_directory(sub_directory)

    def search(self, key_words: List[str]):
        print("*** Searching for %s" % str(key_words))

        first_key = key_words[0]
        results = set(self._data_store.get(first_key))

        for i in range(1,len(key_words)):
            candidate_results = self._data_store.get(key_words[i])
            if not candidate_results:
                results = None
                break
            results = results.intersection(set(candidate_results))

        print("*** Results:")

        if results:
            print(str(results).replace(", ", ",\n"))
        else:
            print("No results found")

    def _put_data(self, words: List[str], file: str):
        for word in words:
            files = self._data_store.get(word)
            if not files:
                files = []
            files.append(file)
            self._data_store.put(word, files)

    def show_db(self):
        self._data_store.show_db()