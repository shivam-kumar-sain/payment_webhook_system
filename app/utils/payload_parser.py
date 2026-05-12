def parse_payment_payload(payload):

    return {
        "event_id": payload["id"],
        "event_type": payload["event"],
        "payment_id": payload["payload"]["payment"]["entity"]["id"],
        "payload": payload
    }