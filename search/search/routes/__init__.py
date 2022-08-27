from fastapi import APIRouter

from search.routes.search import router as search_router
from search.routes.venues import router as venues_router

router = APIRouter(prefix="/api")
router.include_router(search_router, prefix="/search")
router.include_router(venues_router, prefix="/venues")
