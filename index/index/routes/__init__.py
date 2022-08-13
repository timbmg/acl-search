from fastapi import APIRouter

from index.routes.index import router as index_router

router = APIRouter(prefix="/api")
router.include_router(index_router, prefix="/index")
