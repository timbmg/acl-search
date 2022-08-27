from typing import Dict, List
from fastapi import APIRouter, Depends

from search.core import ElasticSearchClient

router = APIRouter()


@router.get("", response_model=List[Dict])
def get_venues(elasticsearch_client=Depends(ElasticSearchClient)):
    return elasticsearch_client.get_venues()
