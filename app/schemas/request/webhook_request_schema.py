from pydantic import BaseModel
from typing import Optional


class PaymentEntitySchema(BaseModel):
    id: str
    status: str
    amount: int
    currency: str


class PaymentDataSchema(BaseModel):
    entity: PaymentEntitySchema


class PayloadSchema(BaseModel):
    payment: PaymentDataSchema


class WebhookRequestSchema(BaseModel):
    event: str
    payload: PayloadSchema
    created_at: int
    id: str