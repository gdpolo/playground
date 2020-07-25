from typing import Optional, List


class TrieNode:
    def __init__(self, value):
        self.value = None
        self.children = {}


class Trie:
    def __init__(self):
        self.root = TrieNode("root")

    def insert_word(self, word: str):
        if not word:
            return

        node = self.root

        for c in word.lower():
            if not c in node.children:
                node.children[c] = TrieNode(c)

            node = node.children[c]

        node.value = word

    def find_words_with_prefix(self, prefix: str) -> List[str]:
        # Find common prefix node for all words that start with this prefix
        prefix_node = self.root
        for c in prefix.lower():
            if not c in prefix_node.children:
                return []
            prefix_node = prefix_node.children[c]

        # Now do a bfs to find all leaf words that start with this prefix
        return self._find_leaf_words(prefix_node)

    def _find_leaf_words(self, node: TrieNode) -> List[str]:
        if not node.children:
            return [node.value]
        words = []

        for char, childNode in node.children.items():
            words.extend(self._find_leaf_words(childNode))

        return words
