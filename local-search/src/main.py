from src.local_search.local_search import LocalSearch
from src.utils.log_time import log_time
from os import environ
from os.path import join

'''
todo 
    - autocompletion, similar words, trie
    - case sensitivity
    - Parallel computation
    - Measure performance 
    - mongo DB, scale
    - configure ignore files/dir
    - configure ignore prefix (home)
'''

def _test_dev_games():
    local_search = LocalSearch()
    local_search.index_directory(join(environ['HOME'], "dev", "games"))
    local_search.show_db()
    local_search.search(["games"])
    local_search.search(["troll"])
    local_search.search(["games", "iso"])
    local_search.search(["games", "isotiles"])

@log_time
def _test_documents():
    local_search = LocalSearch()
    local_search.index_directory(join(environ['HOME'], "Documents"))
    local_search._data_store.export_to_file("/tmp/local_search_index.json")
    #local_search._data_store.import_from_file("/tmp/local_search_index.json")

@log_time
# 220 s -> no parallelism
def _test_all():
    local_search = LocalSearch()
    local_search.index_directory("/")

def main():
    # _test_all()
    _test_documents()

if __name__ == '__main__':
    main()
