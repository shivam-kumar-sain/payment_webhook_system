# from fastapi import APIRouter, Request, Depends
# from sqlalchemy.orm import Session
# from app.core.database import get_db
# from app.services.payment_webhook_service import PaymentWebhookService
# from app.schemas.request.webhook_request_schema import (WebhookRequestSchema)

# router = APIRouter(prefix="/webhook", tags=["Webhook"])

# @router.post("/payments")
# async def receive_payment_webhook(payload: WebhookRequestSchema,request: Request,db: Session = Depends(get_db)):
#     service = PaymentWebhookService(db)
#     return await service.process_webhook(request=request,payload=payload)


from typing import Union, List
from fastapi import (APIRouter,Request,Depends)
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.payment_webhook_service import (PaymentWebhookService)
from app.schemas.request.webhook_request_schema import (WebhookRequestSchema)

router = APIRouter(prefix="/webhook",tags=["Webhook"])

@router.post("/payments")
async def receive_payment_webhook(payload: Union[WebhookRequestSchema,List[WebhookRequestSchema]],request: Request,db: Session = Depends(get_db)):
    service = PaymentWebhookService(db)
    """
        ------------------------------------------
        Bulk Webhook Support
        ------------------------------------------
    """
    if isinstance(payload, list):
        payload_data = [item.model_dump()for item in payload]
        return service.process_bulk_webhooks(payload_data)

    """
        ------------------------------------------
        Single Webhook Support
        ------------------------------------------
    """

    return await service.process_webhook(request=request,payload=payload)