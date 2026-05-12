from sqlalchemy import String, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from core.database import Base


class PaymentEvent(Base):
    __tablename__ = "payment_events"


    event_id: Mapped[str] = mapped_column(String,unique=True,nullable=False)
    payment_id: Mapped[str] = mapped_column(String,index=True,nullable=False)
    event_type: Mapped[str] = mapped_column(String,nullable=False)
    payload: Mapped[dict] = mapped_column(JSON,nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)