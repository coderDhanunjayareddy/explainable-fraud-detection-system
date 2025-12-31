from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.router import api_router
from app.core.exceptions import AppException, app_exception_handler
from app.db.init_db import init_db

def create_app() -> FastAPI:
    setup_logging()
    init_db()
    
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.ENV != "production"
    )

    app.include_router(api_router)
    app.add_exception_handler(AppException, app_exception_handler)
    
    return app

app = create_app()