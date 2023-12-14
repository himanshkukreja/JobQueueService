from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class JobStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"


class Job(BaseModel):
    id: str
    status: JobStatus = JobStatus.PENDING.value
    numberOfAttempts: int = 0
    timestamp: str

# Define the Response Data model
class ResponseData(BaseModel):
    jobs: List[Job]
    total_jobs_returned: int

# Define the API Response model
class ApiResponse(BaseModel):
    message: str
    data: Optional[ResponseData]  # Optional, as it might be empty in case of an error

class AddJobResponse(BaseModel):
    message:str
    jobId:str


