from fastapi import APIRouter

from app.api.public.webhook_routes import router as webhook_router
from app.api.private.payment_routes import router as payment_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(webhook_router)
api_router.include_router(payment_router)