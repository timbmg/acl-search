import logging
from typing import Dict, List, Union

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Index
from elasticsearch_dsl.exceptions import ValidationException

from index.models.elasticsearch import File, Publication, Venue
from index.settings import ElasticSearchSettings


logger = logging.getLogger(__name__)


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
        self.create_index_if_not_exists(File)
        self.create_index_if_not_exists(Publication)
        self.create_index_if_not_exists(Venue)

    def create_index_if_not_exists(self, model: Document):
        if not Index(model.Index.name).exists(using=self.es):
            model.init(using=self.es)

    def index_venue(self, venue: Union[Venue, Dict]):
        if isinstance(venue, dict):
            _id = venue.pop("_id")
            venue = Venue(**venue, meta={"id": _id})
        venue.save(using=self.es)

    def index_publication(self, publication: Union[Publication, Dict]):

        logger.info("Indexing publication: {}".format(publication["bibkey"]))

        if isinstance(publication, dict):
            publication = Publication(**publication, meta={"id": publication["bibkey"]})
        try:
            publication.save(using=self.es)
        except ValidationException as e:
            print(f"Skipping {publication}.\n{e}")

    def index_publications(self, publications: List[Union[Publication, Dict]]):
        # TODO: Bulk indexing
        for publication in publications:
            self.index_publication(publication)

    def index_file(self, file: Union[File, Dict]):
        if isinstance(file, Dict):
            file = File(**file, meta={"id": file["name"]})
        file.save(using=self.es)

    def get_file_by_id(self, _id: str) -> Union[None, File]:
        return File.get(id=_id, using=self.es, ignore=404)
