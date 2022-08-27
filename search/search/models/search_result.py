from typing import List

from pydantic import BaseModel

from search.models import Publication


class PublicationSearchResult(BaseModel):
    publication: Publication
    score: float


class PublicationSearchResults(BaseModel):
    search_results: List[PublicationSearchResult]
    took: int
    hits: int
