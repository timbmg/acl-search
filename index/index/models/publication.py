from typing import List
from pydantic import BaseModel, Field


class Author(BaseModel):
    firstname: str
    lastname: str


class Publication(BaseModel):
    title: str
    conference: str
    year: int = Field(..., gt=0)
    bibkey: str
    url: str
    authors: List[Author]
    abstract: str = Field(None)
