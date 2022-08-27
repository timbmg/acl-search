from elasticsearch_dsl import Boolean, Document, Keyword


class Venue(Document):
    class Index:
        name = "venues"
        settings = {
            "number_of_shards": 1,
        }

    acronym = Keyword(required=True)
    name = Keyword(required=True)
    is_acl = Boolean(required=True)
    is_toplevel = Boolean(required=True)
