import unittest
from os import environ
from os.path import join

from local_search.local_search import LocalSearch
from utils.log_time import log_time


class SearchTest(unittest.TestCase):
    def test_tiny(self):
        local_search = LocalSearch()
        local_search.index_directory(join(environ['HOME'], "dev", "games")) # todo - windows is different?
        results = local_search.search(["games"])

    def test_basic(self):
        local_search = LocalSearch()

        local_search.index_directory(join(environ['HOME'], "Documents")) # todo - windows is different?
        results = local_search.search(["book", "2019"])


    @log_time
    def _index_directory(self, local_search: LocalSearch):
        local_search.index_directory(join(environ['HOME'], "Documents")) # todo - windows is different?

