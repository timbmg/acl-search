from elasticsearch_dsl import (
    Document,
    InnerDoc,
    Integer,
    Keyword,
    Nested,
    SearchAsYouType,
    Text,
)


class Author(InnerDoc):
    firstname = Text()
    lastname = Text()


class Publication(Document):
    class Index:
        name = "publications"
        settings = {
            "number_of_shards": 1,
        }

    title = SearchAsYouType(required=True)
    conference = Keyword(required=True)
    year = Integer(required=True)
    volume = Keyword()
    abstract = Text()
    url = Text()
    bibkey = Text()
    authors = Nested(Author, multi=True)
