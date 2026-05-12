from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from services.payment_webhook_service import PaymentWebhookService

router = APIRouter(prefix="/public/webhook", tags=["Webhook"])

@router.post("/payments")
async def receive_payment_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    service = PaymentWebhookService(db)
    return await service.process_webhook(request)