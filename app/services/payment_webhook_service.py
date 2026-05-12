class PaymentWebhookService:

    def __init__(self, db):
        self.db = db
        self.repo = PaymentEventRepository(db)

    async def process_webhook(self, request):

        raw_body = await request.body()

        signature = request.headers.get(
            "X-Razorpay-Signature"
        )

        verify_signature(raw_body, signature)

        payload = await request.json()

        event_id = payload["id"]

        existing = self.repo.get_by_event_id(event_id)

        if existing:
            raise DuplicateWebhookException()

        event_data = parse_payment_payload(payload)

        return self.repo.create(event_data)