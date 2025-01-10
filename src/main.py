from fastapi import FastAPI
from .config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=settings.DOCS_URL,
    description=settings.DESCRIPTION,
    debug=settings.DEBUG,
)
