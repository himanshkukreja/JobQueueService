from fastapi import FastAPI
from logger.logging import get_logger
from services.middlewares import api_timing_middleware
from routes import job_queue

logger = get_logger(__name__)

app = FastAPI()
app.middleware("http")(api_timing_middleware)  

app.include_router(job_queue.router)