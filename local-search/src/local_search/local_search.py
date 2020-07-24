from os.path import basename
from os import walk
from os.path import sep, splitext, join
from typing import List
from hashlib import md5

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
        results = set(self._data_store.get("words", first_key.lower()))

        for i in range(1,len(key_words)):
            candidate_results = self._data_store.get("words", key_words[i].lower())
            if not candidate_results:
                results = None
                break
            results = results.intersection(set(candidate_results))

        print("*** Results:")

        if results:
            # Convert file keys to file paths
            results = [self._data_store.get("files", file_key) for file_key in results]
            print(str(results).replace(", ", ",\n"))
        else:
            print("No results found")
            return "No results found"

        return str(results) # todo - need to wrap as response

    def _put_data(self, words: List[str], file_path: str):
        for word in words:
            word_lc = word.lower()

            # When time comes, this should be a transaction
            files = self._data_store.get("words", word_lc)
            if not files:
                files = []

            # Need to index the file and only save the mdsum of the file in the list

            file_key = self._get_file_key(file_path)
            files.append(file_key)

            self._data_store.put_if_not_exists("files", file_key, file_path)
            self._data_store.put("words", word_lc, files)
            # End of transaction

    def show_db(self):
        self._data_store.show_db()

    def _get_file_key(self, file_path: str) -> str:
        return md5(file_path.encode()).hexdigest()