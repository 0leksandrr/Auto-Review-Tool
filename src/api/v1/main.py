from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1.lifespan import init_message_broker, close_message_broker
from src.api.v1.reviews.handlers import router as router_review
from src.api.v1.assistant.handlers import router as router_assistant
from src.utils.config import settings
from src.utils.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting the message broker...")
        await init_message_broker()
        logger.info("Message broker started successfully.")
        yield
    except Exception as e:
        logger.error(f"Error during lifespan startup: {e}")
        raise
    finally:
        try:
            logger.info("Closing the message broker...")
            await close_message_broker()
            logger.info("Message broker closed successfully.")
        except Exception as e:
            logger.error(f"Error during lifespan shutdown: {e}")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url=settings.DOCS_URL,
        description=settings.DESCRIPTION,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )
    app.include_router(router_review, prefix=settings.API_V1_STR)
    app.include_router(router_assistant, prefix=settings.API_V1_STR)

    return app


app = create_app()
