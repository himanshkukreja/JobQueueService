from fastapi import APIRouter,Query
from db.models.JobQueue import ApiResponse,AddJobResponse,JobStatus
from services import job_queue_services


router = APIRouter(tags=['JobQueue'], prefix="")


@router.post("/addJob",response_model=AddJobResponse)
async def add_job():
    return await job_queue_services.add_job()


@router.get("/status", response_model=ApiResponse)
async def get_status(count: int = Query(10, alias="count", gt=0), status_type:JobStatus= Query(None)):
    return await job_queue_services.get_status(count, status_type)
