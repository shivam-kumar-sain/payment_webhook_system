from app.models.payment_event_model import PaymentEvent
class PaymentEventRepository:

    def __init__(self, db):
        self.db = db

    def get_by_event_id(self, event_id):
        return self.db.query(PaymentEvent).filter(PaymentEvent.event_id == event_id).first()

    def create(self, data):
        obj = PaymentEvent(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj
    
    def get_payment_events(self,payment_id: str):
        return (
            self.db.query(PaymentEvent)
            .filter(PaymentEvent.payment_id == payment_id)
            .order_by(PaymentEvent.received_at.asc()).all()
        )
