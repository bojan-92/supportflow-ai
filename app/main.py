from fastapi import FastAPI, Request
import uuid
from app.api.health import router as health_router
from app.api.ai import router as ai_router
from app.core.logging import configure_logging
from app.api.exception_handlers import (
    register_exception_handlers,
)

configure_logging()

app = FastAPI(
    title="SupportFlow AI",
    version="0.1.0",
)

register_exception_handlers(app)

app.include_router(health_router)
app.include_router(ai_router)

@app.middleware("http")
async def add_request_id(
    request: Request,
    call_next,
):
    request_id = f"sf_{uuid.uuid4().hex}"

    request.state.request_id = request_id

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    return response
