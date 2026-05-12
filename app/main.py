from fastapi import FastAPI, Request,HTTPException
from fastapi.staticfiles import StaticFiles
import uvicorn
from core.logger import get_logger
from api.router import api_router
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import os
import time

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
    return app
    
""" 
    ---------------------------------------------------------
                        Create App
    ---------------------------------------------------------
"""
app = create_application()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount("/static",StaticFiles(directory=os.path.join(BASE_DIR, "static")),name="static",)


app.include_router(api_router)
""" 
    ---------------------------------------------------------
                    Secure OpenAPI JSON
    ---------------------------------------------------------
"""

@app.get("/openapi.json", include_in_schema=False)
def openapi_json():
    return get_openapi(
        title=settings.app_title,
        version=settings.app_version,
        description=settings.app_description,
        routes=app.routes,
    )

""" 
    ---------------------------------------------------------
                        Secure Swagger UI
    ---------------------------------------------------------
"""

@app.get("/docs", include_in_schema=False)
def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=settings.app_title,
        swagger_favicon_url="/static/favicon.ico",
    )

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

