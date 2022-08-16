from typing import Dict, List, Union

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index
from elasticsearch_dsl.exceptions import ValidationException
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

    def index_publication(self, publication: Union[Publication, Dict]):
        if isinstance(publication, dict):
            publication = Publication(**publication, meta={"id": publication["bibkey"]})
        try:
            publication.save(using=self.es)
        except ValidationException as e:
            print(f"Skipping {publication}.\n{e}")
        self.search_publications.cache_clear()

    def index_publications(self, publications: List[Union[Publication, Dict]]):
        # TODO: Bulk indexing
        for publication in publications:
            self.index_publication(publication)
