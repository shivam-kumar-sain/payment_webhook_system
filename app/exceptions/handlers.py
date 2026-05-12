@app.exception_handler(
    InvalidSignatureException
)
async def invalid_signature_handler(
    request,
    exc
):
    return JSONResponse(
        status_code=403,
        content={
            "status": False,
            "message": "Invalid signature"
        }
    )