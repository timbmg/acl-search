from typing import List
from pydantic import BaseModel, Field


class Author(BaseModel):
    firstname: str
    lastname: str


class Publication(BaseModel):
    title: str
    conference_short: str
    conference_long: str
    year: int = Field(..., gt=0)
    bibkey: str
    url: str
    authors: List[Author]
    abstract: str = Field(None)

    @classmethod
    def from_es_source(cls, _source: dict):
        return cls(
            conference_short=_source["conference_short"],
            conference_long=_source["conference_long"],
            year=_source["year"],
            bibkey=_source["bibkey"],
            url=_source["url"],
            title=_source["title"],
            abstract=_source.get("abstract", ""),
            authors=_source["authors"],
        )
