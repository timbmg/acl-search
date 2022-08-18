from typing import List, Optional
from cachetools import cached, TTLCache

from search.core import ElasticSearchClient
from search.models import Publication

elasticsearch_client = ElasticSearchClient()

router = APIRouter()


@cached(cache=TTLCache(maxsize=100, ttl=600))
@router.get("/publications", response_model=List[Publication])
def get_publication(
    query: str,
    from_: Optional[int] = None,
    size: Optional[int] = None,
):
    return elasticsearch_client.search_publications(query, from_=from_, size=size)
