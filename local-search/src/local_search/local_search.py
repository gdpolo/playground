from logging import exception
from os import walk
from os.path import sep, splitext, join
from typing import List, Set
from hashlib import md5

from database.KeyValuePair import KeyValuePair
from database.trie import Trie
from database.mongo_data_store import MongoDataStore #todo - use factory

# TODO - ignore directories or files


class BulkWriterService:
    def __init__(self, data_store: MongoDataStore, batch_size: int = 1000):
        self.batch_size=batch_size
        self.requests_by_entity = {}
        self.data_store = data_store

    def write_bulk(self, entity: str, data: List[KeyValuePair]):
        if entity not in self.requests_by_entity:
            self.requests_by_entity[entity] = []

        missing_requests_for_flush = self.batch_size - len(self.requests_by_entity[entity])

        for i in range(min(missing_requests_for_flush, len(data))):
            self.requests_by_entity[entity].append(data[i])

        if len(self.requests_by_entity[entity]) == self.batch_size:
            self.flush_entity(entity)

            for i in range(missing_requests_for_flush, len(data)):
                self.requests_by_entity[entity].append(data[i])

    def flush_entity(self, entity: str):
        print("flush " + entity)
        self.data_store.bulk_write(entity, self.requests_by_entity[entity])
        self.requests_by_entity[entity] = []

    def flush_all(self):
        for entity, data in self.requests_by_entity.items():
            self.data_store.bulk_write(entity, data)
            self.requests_by_entity[entity] = []

class LocalSearch:
    def __init__(self):
        self._data_store = MongoDataStore(["words", "files"])
        self._bulk_writer_service = BulkWriterService(self._data_store)
        self.trie = Trie()
        self.expected_words_count = 0
        self.expected_files_count = 0

    def index_directory(self, root_dir: str):
        self._data_store.clear()
        self.index_directory_internal(root_dir)
        self._bulk_writer_service.flush_all()

        print( "Expected words count:", self.expected_words_count)
        print( "Expected files count:", self.expected_files_count)

    def index_directory_internal(self, root_dir: str):

        # Index given directoy
        for directory, subdir_list, file_list in walk(root_dir):
            words = list(directory.split(sep))
            all_directory_files_data = []
            all_directory_words_data = []

            for file_name in file_list:
                file_name_without_extension = splitext(file_name)[0]
                file_path = join(directory, file_name)
                files_data, words_data = self._prepare_data_for_bulk_write(words + [file_name_without_extension], file_path)
                all_directory_files_data.extend(files_data)
                all_directory_words_data.extend(words_data)

            self.expected_files_count += len(file_list)
            self.expected_words_count += len(words) #+ len(file_list)

            self._bulk_writer_service.write_bulk("files", all_directory_files_data)
            self._bulk_writer_service.write_bulk("words", all_directory_words_data)

            for sub_directory in subdir_list:
                self.index_directory_internal(sub_directory)


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
            if word == "":
                continue

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

    def _prepare_data_for_bulk_write(self, words: List[str], file_path: str):
        words_data = []
        files_data = []
        # Can parallelize this
        for word in words:
            if word == "":
                continue

            word_lc = word.lower()
            self.trie.insert_word(word_lc)

            #files = self._data_store.get("words", word_lc)
            #if not files:
            #    files = []

            file_key = self._get_file_key(file_path)
            #files.append(file_key)

            files_data.append(KeyValuePair(file_key, file_path))
            words_data.append(KeyValuePair(word_lc, [file_key])) # This can't be easily abstracted for memory data store
        return files_data, words_data

    def show_db(self):
        self._data_store.show_db()

    def _get_file_key(self, file_path: str) -> str:
        return md5(file_path.encode()).hexdigest()