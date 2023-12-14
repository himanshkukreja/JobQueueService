import time
from fastapi import Request
from logger.logging import get_logger

logger = get_logger(__name__)

async def api_timing_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    # Logging the API call and its execution time
    logger.info(f"API call: {request.url.path} completed in {process_time} seconds")
    response.headers["X-Process-Time"] = str(process_time)
    return response

