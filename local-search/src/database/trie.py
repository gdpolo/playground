from typing import List


class TrieNode:
    __slots__ = "children", "is_word"

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
            code = self._char_to_key(c)
            if not code in node.children:
                node.children[code] = TrieNode()

            node = node.children[code]
        node.is_word = True

    def find_words_with_prefix(self, prefix: str) -> List[str]:
        # Find common prefix node for all words that start with this prefix
        prefix_node = self.root
        for c in prefix.lower():
            code = self._char_to_key(c)
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
            words.extend(self._find_leaf_words("".join([prefix, self._key_to_char(code)]), childNode))

        return words

    def _char_to_key(self, char):
        return ord(char)

    def _key_to_char(self, key):
        return chr(key)