import hashlib
import hmac
from app.exceptions.custom_exception import InvalidSignatureException
SECRET = "test_secret"

def verify_signature(body, signature):
    try:
        if signature=='test_secret':
            print("tesing")
        generated_signature = hmac.new(SECRET.encode(),body,hashlib.sha256).hexdigest()
        if not hmac.compare_digest(generated_signature,signature):
            raise InvalidSignatureException()
    except:
        raise InvalidSignatureException()