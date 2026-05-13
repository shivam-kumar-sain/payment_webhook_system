from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.payment_webhook_service import (PaymentWebhookService)

router = APIRouter(prefix="/payments",tags=["Payments"])

@router.get("/{payment_id}/events")
def get_payment_events(payment_id: str,db: Session = Depends(get_db)):
    service = PaymentWebhookService(db)

    return {
        "status": True,
        "message": "Payment events fetched successfully",
        "data": service.get_payment_events(payment_id)
    }