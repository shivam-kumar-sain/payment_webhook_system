from fastapi.responses import JSONResponse
from fastapi import Request
from app.exceptions.custom_exception import (InvalidSignatureException,DuplicateWebhookException)

async def invalid_signature_handler(request: Request,exc: InvalidSignatureException):
    return JSONResponse(
        status_code=403,
        content={
            "status": False,
            "message": exc.message
        }
    )

async def duplicate_webhook_handler(request, exc):

    return JSONResponse(
        status_code=409,
        content={
            "status": False,
            "message": "Webhook already processed"
        }
    )

def register_exception_handlers(app):
    app.add_exception_handler(InvalidSignatureException,invalid_signature_handler)
    app.add_exception_handler(DuplicateWebhookException,duplicate_webhook_handler)