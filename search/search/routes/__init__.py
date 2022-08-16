from fastapi import APIRouter

from search.routes.search import router as search_router

router = APIRouter(prefix="/api")
router.include_router(search_router, prefix="/search")
