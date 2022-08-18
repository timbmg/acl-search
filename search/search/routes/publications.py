from typing import Dict, List
from fastapi import APIRouter

from search.core import ElasticSearchClient

elasticsearch_client = ElasticSearchClient()

router = APIRouter()


@router.get("/conferences", response_model=List[str])
def get_conferences():
    conferences_to_counts = elasticsearch_client.get_unique_value_conuts(
        index="publications", field="conference_short"
    )
    return list(conferences_to_counts.keys())
