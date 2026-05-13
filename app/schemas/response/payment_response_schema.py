from pydantic import BaseModel
from datetime import datetime


class PaymentEventResponse(BaseModel):
    event_type: str
    received_at: datetime

    class Config:
        from_attributes = True