from src.local_search.local_search import LocalSearch

#todo - autocompletion, similar words, trie

def main():
    local_search = LocalSearch()
    local_search.index_directory("/home/tsampinho/dev/games")
    local_search.show_db()
    local_search.search(["games"])
    local_search.search(["troll"])
    local_search.search(["games", "iso"])
    local_search.search(["games", "isotiles"])

if __name__ == '__main__':
    main()
