import unittest

from local_search.trie import Trie


class TestTrie(unittest.TestCase):
    def test_basic(self):
        trie = Trie()
        trie.insert_word("america")
        trie.insert_word("amazon")
        trie.insert_word("amore")

        assert set(trie.find_words_with_prefix("am")) == {'america', 'amazon', 'amore'}
        assert set(trie.find_words_with_prefix("amo")) == {'amore'}
        assert trie.find_words_with_prefix("b") == []

    def test_more_than_one_root(self):
        trie = Trie()
        trie.insert_word("america")
        trie.insert_word("amazon")
        trie.insert_word("amore")
        trie.insert_word("big")
        trie.insert_word("book")

        assert set(trie.find_words_with_prefix("am")) == {'america', 'amazon', 'amore'}
        assert set(trie.find_words_with_prefix("amo")) == {'amore'}
        assert set(trie.find_words_with_prefix("b")) == {'big', 'book'}
