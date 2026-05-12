import hashlib
import hmac

SECRET = "test_secret"

def verify_signature(body, signature):

    generated_signature = hmac.new(
        SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(
        generated_signature,
        signature
    ):
        raise InvalidSignatureException()