from elasticsearch_dsl import Document, Keyword, Integer


class File(Document):
    class Index:
        name = "files"
        settings = {
            "number_of_shards": 1,
        }

    name = Keyword(required=True)
    last_modified = Integer(required=True)
