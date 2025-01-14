from fastapi import FastAPI

from src.api.v1.reviews.handlers import router as router_review
from src.api.v1.assistant.handlers import router as router_assistant
from src.utils.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url=settings.DOCS_URL,
        description=settings.DESCRIPTION,
        debug=settings.DEBUG,
    )
    app.include_router(router_review, prefix=settings.API_V1_STR)
    app.include_router(router_assistant, prefix=settings.API_V1_STR)

    return app


app = create_app()
