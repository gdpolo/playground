from typing import Optional, List


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert_word(self, word: str):
        if not word:
            return

        node = self.root

        for c in word.lower():
            code = ord(c)
            if not code in node.children:
                node.children[code] = TrieNode()

            node = node.children[code]
        node.is_word = True

    def find_words_with_prefix(self, prefix: str) -> List[str]:
        # Find common prefix node for all words that start with this prefix
        prefix_node = self.root
        for c in prefix.lower():
            code = ord(c)
            if not code in prefix_node.children:
                return []

            prefix_node = prefix_node.children[code]

        # Now do a bfs to find all leaf words that start with this prefix
        return self._find_leaf_words(prefix, prefix_node)

    def _find_leaf_words(self, prefix: str, node: TrieNode) -> List[str]:
        words = []
        if node.is_word:
            words.append(prefix)

        for code, childNode in node.children.items():
            words.extend(self._find_leaf_words(prefix + chr(code), childNode))

        return words
