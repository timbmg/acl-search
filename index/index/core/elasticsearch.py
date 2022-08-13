from typing import Dict, List
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index
from elasticsearch_dsl.query import MultiMatch

from index.models.elasticsearch.publication import Publication
from index.settings import ElasticSearchSettings


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
        self.create_publications_index_if_not_exists()

    def create_publications_index_if_not_exists(self):
        if not Index("publications").exists(using=self.es):
            Publication.init(using=self.es)

    def index_publication(self, publication: Dict):
        publication = Publication(**publication)
        publication.save(using=self.es)

    def index_publications(self, publications: List[Dict]):
        # TODO: Bulk indexing
        for publication in publications:
            publication = Publication(**publication)
            self.add_publication(publication)

    def search_publications(self, query: str):
        s = Publication.search(using=self.es)

        s.query = MultiMatch(
            query=query,
            type="bool_prefix",
            fields=["title"],
        )
        response = s.execute()

        return [p.to_dict() for p in response]
