from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from cachetools import cached, TTLCache

from search.core import ElasticSearchClient
from search.models import Publication
router = APIRouter()


@cached(cache=TTLCache(maxsize=100, ttl=600))
@router.get("/publications", response_model=List[Publication])
def get_publication(
    query: str,
    conferences: Optional[List[str]] = Query(
        None,
        description="List of conferences to include, or if starting with `-` exclude.",
    ),
    year_gte: Optional[int] = Query(
        None, description="The year from which to include publications."
    ),
    year_lte: Optional[int] = Query(
        None, description="The year up to which to include publications."
    ),
    from_: Optional[int] = None,
    size: Optional[int] = None,
    elasticsearch_client=Depends(ElasticSearchClient),
):
    conferences_to_include, conferences_to_exclude = [], []
    if conferences:
        for c in conferences:
            if c.startswith("-"):
                conferences_to_exclude.append(c[1:])
            else:
                conferences_to_include.append(c)

    conferences_to_include = conferences_to_include or None
    conferences_to_exclude = conferences_to_exclude or None

    return elasticsearch_client.search_publications(
        query=query,
        conferences_to_include=conferences_to_include,
        conferences_to_exclude=conferences_to_exclude,
        year_gte=year_gte,
        year_lte=year_lte,
        from_=from_,
        size=size,
    )
