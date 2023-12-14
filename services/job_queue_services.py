
from fastapi import HTTPException
from uuid import uuid4
from datetime import datetime
from logger.logging import get_logger
from db import db_actions
from db.models.JobQueue import Job,ApiResponse,ResponseData,AddJobResponse
from services.sqs_services import publish_job


logger = get_logger(__name__)


async def add_job():
    job_id = str(uuid4())
    current_timestamp = datetime.utcnow().isoformat()  
    job = Job(id=job_id, timestamp=current_timestamp)
    job_dic = job.model_dump()
    db_actions.insert_into_jobs(job_dic)
    logger.debug(f"Pushing the job to the queue with Id {job_id}")
    
    try:
        publish_job(job_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

    response = AddJobResponse(message="Job added", jobId=job_id)
    return response



async def get_status(count: int, status_type:str):
    try:
        if not status_type:
            jobs_data = db_actions.find_jobs()
        else:
            jobs_data = db_actions.find_jobs_by_status(status_type)

        jobs_data = list(jobs_data.sort("timestamp", -1).limit(count))
        jobs = []
        for job in jobs_data:
            job_model = Job(
                id=job.get('id', ''), 
                status=job.get('status', ''),
                numberOfAttempts=job.get('numberOfAttempts', 0),
                timestamp=job.get('timestamp', '')
            )
            jobs.append(job_model)
        response_data = ResponseData(jobs=jobs, total_jobs_returned=len(jobs))
        return ApiResponse(message="Retrieved latest jobs", data=response_data)
    except Exception as e:
        return ApiResponse(message=str(e), data=None)
    