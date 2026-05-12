class PaymentEvent(Base):

    __tablename__ = "payment_events"

    id = Column(Integer, primary_key=True)

    event_id = Column(String, unique=True, nullable=False)

    payment_id = Column(String, index=True)

    event_type = Column(String)

    payload = Column(JSON)

    received_at = Column(DateTime)