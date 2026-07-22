import time
import logging
from uuid import uuid4

from fastapi import FastAPI, Request


logger = logging.getLogger(__name__)


def register_middlewares(app: FastAPI) -> None:
    @app.middleware("http")
    async def request_context_middleware(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.6f}"
        logger.info(
            "request_id=%s method=%s path=%s status_code=%s process_time=%.6f",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )
        return response
