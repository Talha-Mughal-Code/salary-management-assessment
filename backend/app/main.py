from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.tags import TAGS_METADATA

app = FastAPI(
    title="Salary Management API", version="0.1.0", openapi_tags=TAGS_METADATA
)
app.include_router(health_router)
