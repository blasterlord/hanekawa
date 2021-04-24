from pathlib import Path

from whoosh.fields import Schema, STORED, TEXT
from whoosh.highlight import ContextFragmenter, NullFormatter
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser


class SearchEngine:
    def __init__(self):
        schema = Schema(filename=STORED, arc=STORED, content=TEXT)

        # Index creation
        index_dir_name = "index"
        index_dir_path = Path.cwd().joinpath(index_dir_name)
        self.content_dir_path = Path.cwd().joinpath("content")
        if index_dir_path.exists():
            self.index = open_dir(index_dir_name)
        else:
            index_dir_path.mkdir()
            self.index = create_in(index_dir_name, schema)
            index_writer = self.index.writer()
            for document_path in self.content_dir_path.glob("*.txt"):
                print(document_path.as_posix())
                with open(document_path, encoding="utf-8", errors="ignore") as file_object:
                    index_writer.add_document(filename=document_path.name, arc=document_path.stem,
                                              content=file_object.read())
            index_writer.commit()

    def search(self, query_string: str):
        parser = QueryParser("content", self.index.schema)
        query = parser.parse(query_string)
        with self.index.searcher() as searcher:
            results = searcher.search(query)
            results.fragmenter = ContextFragmenter(charlimit=None, maxchars=190, surround=80)
            results.highlighter.formatter = NullFormatter()
            cached_file_contents = {}
            for hit in results:
                filename = hit["filename"]
                if filename in cached_file_contents:
                    file_contents = cached_file_contents[filename]
                else:
                    with open(self.content_dir_path.joinpath(filename), encoding="utf-8") as file_object:
                        file_contents = file_object.read()
                    cached_file_contents[filename] = file_contents

                print(hit["arc"])
                for entry in hit.highlights("content", text=file_contents, top=10).split("..."):
                    entry = entry.replace("\n\n", "\n")
                    print("{entry}\n".format(entry=entry))
