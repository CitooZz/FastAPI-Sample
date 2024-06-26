from fastapi.routing import APIRouter
from rukita.web.api import monitoring, product

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(product.router)
