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

    venue_short = Keyword(required=True)
    venue_long = Keyword(required=True)
    year = Integer(required=True)
    bibkey = Text(required=True)
    url = Text(required=True)
    title = SearchAsYouType(required=True)
    abstract = Text(required=False)
    authors = Nested(Author, multi=True, required=True)
