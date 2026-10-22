from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.employees import router as employees_router
from app.api.errors import register_error_handlers
from app.api.health import router as health_router
from app.api.insights import router as insights_router
from app.api.tags import TAGS_METADATA

app = FastAPI(
    title="Salary Management API", version="0.1.0", openapi_tags=TAGS_METADATA
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type"],
    expose_headers=["Content-Disposition"],
)
app.include_router(health_router)
app.include_router(employees_router)
app.include_router(insights_router)
register_error_handlers(app)
