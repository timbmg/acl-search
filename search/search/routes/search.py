from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from cachetools import cached, TTLCache

from search.core import ElasticSearchClient
from search.models import PublicationSearchResults

router = APIRouter()


@cached(cache=TTLCache(maxsize=1024, ttl=600))
@router.get("/publications", response_model=PublicationSearchResults)
def get_publication(
    query: str,
    venues: Optional[List[str]] = Query(
        None,
        description="List of venues to include, or if starting with `-` exclude.",
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
    venues_to_include, venues_to_exclude = [], []
    if venues:
        for v in venues:
            # HACK: Somehow ES has indexed the venues in lowercase, 
            # so we need to lower them here.
            v = v.lower()
            if v.startswith("-"):
                venues_to_exclude.append(v[1:])
            else:
                venues_to_include.append(v)

    venues_to_include = venues_to_include or None
    venues_to_exclude = venues_to_exclude or None

    return elasticsearch_client.search_publications(
        query=query,
        venues_to_include=venues_to_include,
        venues_to_exclude=venues_to_exclude,
        year_gte=year_gte,
        year_lte=year_lte,
        from_=from_,
        size=size,
    )
