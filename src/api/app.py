import logging

from fastapi import Depends, FastAPI, Response, status
from sqlalchemy.orm import Session

from src.api import deps
from src.api.chat import router as chat_router
from src.config import Config


def create_app(config: Config):
    app = FastAPI(
        title=config.PROJECT_NAME,
    )

    app.include_router(chat_router)

    @app.get("/livez", status_code=status.HTTP_200_OK, response_class=Response)
    def livez():
        pass

    @app.get("/readyz", status_code=status.HTTP_200_OK, response_class=Response)
    def readyz(db: Session = Depends(deps.get_db)):
        pass

    @app.on_event("startup")
    def startup_event():
        logger_name = "uvicorn"
        logger = logging.getLogger(logger_name)
        logger.handlers = []
        logger_name = "uvicorn.access"
        logger = logging.getLogger(logger_name)
        logger.handlers = []

    return app
