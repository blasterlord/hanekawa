from core.search_engine import SearchEngine

if __name__ == "__main__":
    search_engine = SearchEngine()
    while True:
        query_string = input("Enter a search string ")
        if query_string == "q":
            break
        search_engine.search(query_string)
