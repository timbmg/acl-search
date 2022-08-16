from functools import lru_cache
from elasticsearch import Elasticsearch
from elasticsearch_dsl.query import MultiMatch


from search.models.elasticsearch import Publication
from search.settings import ElasticSearchSettings


class ElasticSearchClient:
    def __init__(self) -> None:
        self.settings = ElasticSearchSettings()
        self.es = Elasticsearch(
            hosts=[self.settings.connection_string],
            timeout=self.settings.timeout,
            retry_on_timeout=self.settings.retry_on_timeout,
            max_retries=self.settings.max_retries,
            sniff_on_start=True,
            sniff_on_connection_fail=True,
        )

    @lru_cache(maxsize=128)
    def search_publications(self, query: str, from_: int = None, size: int = None):
        s = Publication.search(using=self.es)

        extra_params = {}
        if from_ is not None:
            extra_params["from_"] = from_
        if size is not None:
            extra_params["size"] = size
        if extra_params:
            s = s.extra(**extra_params)

        s.query = MultiMatch(
            query=query,
            type="bool_prefix",
            fields=["title"],
        )
        response = s.execute()

        return [p.to_dict() for p in response]

    def reset_search_publications_cache(self):
        self.search_publications.cache_clear()
