from typing import List, Optional
from fastapi import APIRouter

from search.core import ElasticSearchClient
from search.models import Publication

elasticsearch_client = ElasticSearchClient()

router = APIRouter()


@router.get("/publications", response_model=List[Publication])
def get_publication(
    query: str,
    from_: Optional[int] = None,
    size: Optional[int] = None,
):
    return elasticsearch_client.search_publications(query, from_=from_, size=size)
