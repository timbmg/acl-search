from fastapi import APIRouter

from index.routes.index import router as index_router
from index.routes.publications import router as publications_router

router = APIRouter(prefix="/api")
router.include_router(index_router, prefix="/index")
router.include_router(publications_router, prefix="/publications")
