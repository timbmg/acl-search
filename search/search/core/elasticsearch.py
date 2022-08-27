import logging
from typing import Dict, List, Optional
from elasticsearch import Elasticsearch
from elasticsearch_dsl import A, Search
from elasticsearch_dsl.query import Bool, MultiMatch, MatchAll


from search.models.elasticsearch import Publication as ESPublication, Venue as ESVenue
from search.models import PublicationSearchResults, PublicationSearchResult, Publication
from search.settings import ElasticSearchSettings

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

    def _es_search_response_to_publication_search_results(
        self, response: Dict
    ) -> PublicationSearchResults:
        search_results = [
            PublicationSearchResult(
                publication=Publication.from_es_source(p["_source"]),
                score=p["_score"],
            )
            for p in response["hits"]["hits"]
        ]
        return PublicationSearchResults(
            search_results=search_results,
            took=response["took"],
            hits=response["hits"]["total"]["value"],
        )

    def search_publications(
        self,
        query: str,
        venues_to_include: Optional[List[str]] = None,
        venues_to_exclude: Optional[List[str]] = None,
        year_gte: Optional[int] = None,
        year_lte: Optional[int] = None,
        from_: Optional[int] = None,
        size: Optional[int] = None,
    ) -> PublicationSearchResults:

        s = ESPublication.search(using=self.es)

        s.query = Bool(
            must=[
                MultiMatch(
                    query=query,
                    type="bool_prefix",
                    fields=["title", "title._2gram", "title._3gram"],
                )
            ]
        )

        extra_params = {}
        if from_ is not None:
            extra_params["from_"] = from_
        if size is not None:
            extra_params["size"] = size
        if extra_params:
            s = s.extra(**extra_params)
        if venues_to_include:
            s = s.filter("terms", venue_short=venues_to_include)
        if venues_to_exclude:
            s = s.exclude("terms", venue_short=venues_to_exclude)
        if year_gte:
            s = s.filter("range", year={"gte": year_gte})
        if year_lte:
            s = s.filter("range", year={"lte": year_lte})

        logger.info("Query: {}".format(s.to_dict()))

        response = s.execute()

        logger.info("Response: {}".format(response.to_dict()))

        return self._es_search_response_to_publication_search_results(
            response.to_dict()
        )

    def get_unique_value_conuts(self, index: str, field: str) -> Dict[str, int]:
        s = Search(using=self.es, index=index)
        a = A("terms", field=field)
        s.aggs.bucket("unique_values", a)
        response = s.execute()
        response = response.to_dict()
        value_to_count = {
            b["key"]: b["doc_count"]
            for b in response["aggregations"]["unique_values"]["buckets"]
        }
        return value_to_count

    def get_venues(self) -> List[Dict]:
        s = ESVenue.search(using=self.es)
        s.query = MatchAll()
        total = s.count()
        s = s[0:total]
        response = s.execute()
        return [r.to_dict() for r in response]
