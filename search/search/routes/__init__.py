from fastapi import APIRouter

from search.routes.search import router as search_router
from search.routes.publications import router as publications_router

router = APIRouter(prefix="/api")
router.include_router(search_router, prefix="/search")
router.include_router(publications_router, prefix="/publications")
