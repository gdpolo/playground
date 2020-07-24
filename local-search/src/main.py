from src.local_search.local_search import LocalSearch
from src.utils.log_time import log_time
from os import environ
from os.path import join, exists

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
def _init_search_engine(root_dir: str, search_index_path: str, force_build_index=False):
    local_search = LocalSearch()
    if force_build_index or not exists(search_index_path):
        local_search.index_directory(root_dir) # todo - windows is different?
        local_search._data_store.export_to_file(search_index_path)
    else:
        local_search._data_store.import_from_file(search_index_path)

    return local_search

@log_time
# 220 s -> no parallelism
# 443 s -> when saving both words and files
# Read in 19 s
def _test_all():
    #local_search = _init_search_engine(join(environ['HOME'], "dev", "games"), "/tmp/local_search_index.json")
    local_search = _init_search_engine("/", "/tmp/local_search_index.json")
    local_search.search(["games"])
    local_search.search(["troll"])
    local_search.search(["games", "iso"])
    local_search.search(["games", "isotiles"])

def main():
    _test_all()

if __name__ == '__main__':
    main()
