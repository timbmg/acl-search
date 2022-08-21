from typing import List
from fastapi import APIRouter, Depends

from search.core import ElasticSearchClient

router = APIRouter()


@router.get("/conferences", response_model=List[str])
def get_conferences(elasticsearch_client=Depends(ElasticSearchClient)):
    conferences_to_counts = elasticsearch_client.get_unique_value_conuts(
        index="publications", field="conference_short"
    )
    return list(conferences_to_counts.keys())
