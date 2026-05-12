from fastapi import FastAPI, Request,HTTPException
import uvicorn
from core.logger import get_logger
from api.router import api_router
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware

import os
import time
app = FastAPI()

app.include_router(api_router)

""" 
    ---------------------------------------------------------
                        Logger
    ---------------------------------------------------------
""" 
logger = get_logger(__name__)
logger.setLevel(settings.log_level)

""" 
    ---------------------------------------------------------
                    App Factory
    ---------------------------------------------------------
"""
def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.app_description,
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    """ 
        -----------------------------------------------------
                        CORS
        -----------------------------------------------------
    """ 
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    """ 
        -----------------------------------------------------
            Request Logging Middleware
        -----------------------------------------------------
    """
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
        except Exception:
            logger.exception("Unhandled exception occurred")
            raise

        process_time = round(time.time() - start_time, 4)
        logger.info(
            f"{request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Time: {process_time}s"
        )
        return response
    
    """ 
        -----------------------------------------------------
        Security Headers Middleware
        -----------------------------------------------------
    """ 
    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        if not request.url.path.startswith(("/docs", "/openapi.json", "/static")):
            response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response
    
""" 
    ---------------------------------------------------------
                        Create App
    ---------------------------------------------------------
"""
app = create_application()


""" 
    ---------------------------------------------------------
                    Run Server
    ---------------------------------------------------------
"""
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )

