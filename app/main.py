from fastapi import FastAPI

from app.core.logging import setup_logging
from app.core.config import settings
from app.api.health import router as health_router
from app.api.documents import router as documents_router



setup_logging()


app = FastAPI(
    title=settings.APP_NAME
)


@app.get("/")
def root():

    return {
        "message": "RAG API running"
    }

app.include_router(
    health_router
)

app.include_router(documents_router)