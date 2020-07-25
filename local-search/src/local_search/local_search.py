from os.path import basename
from os import walk
from os.path import sep, splitext, join
from typing import List, Set
from hashlib import md5

from local_search.trie import Trie
from src.local_search.dict_data_store import DictDataStore

# TODO - ignore directories or files


class LocalSearch:
    def __init__(self):
        self._data_store = DictDataStore()
        self.trie = Trie()

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

    def load_index_from_file(self, file_path: str):
        self._data_store.import_from_file(file_path)

        for word in self._data_store.get_all_keys("words"):
            self.trie.insert_word(word)

    def _search_single_prefix(self, prefix: str) -> Set[any]:
        key_words_with_prefix = self.trie.find_words_with_prefix(prefix)

        results = set()

        if not key_words_with_prefix:
            return results

        for word in key_words_with_prefix:
            keyword_results = self._data_store.get("words", word.lower())
            if keyword_results: # todo - by design there should always be results for all words in the trie
                results = results.union(set(keyword_results))

        return results

    def search(self, prefixes: List[str]):
        print("*** Searching for %s" % str(prefixes))

        if not prefixes:
            print("No results found")
            return "No results found"

        first_prefix = prefixes[0]
        results = self._search_single_prefix(first_prefix)

        if not results:
            print("No results found")
            return "No results found"

        for i in range(1,len(prefixes)):
            candidate_results = self._search_single_prefix(prefixes[i])
            if not candidate_results:
                results = None
                break
            results = results.intersection(set(candidate_results))

        print("*** Results:")

        if results:
            # Convert file keys to file paths
            results = [self._data_store.get("files", file_key) for file_key in results]
            str_results = str(results).replace(", ", ",\n")
            print(str_results)
            return str_results  # todo - need to wrap as response
        else:
            print("No results found")
            return "No results found"

    def _put_data(self, words: List[str], file_path: str):
        for word in words:
            word_lc = word.lower()
            self.trie.insert_word(word_lc)

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