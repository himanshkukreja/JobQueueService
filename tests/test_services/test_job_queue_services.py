
import pytest
from unittest import mock
from services import job_queue_services  # Adjusted import statement
from db.models.JobQueue import Job


@pytest.mark.asyncio
async def test_add_job():
    with mock.patch('app.services.job_queue_services.publish_job') as mock_publish, \
         mock.patch('app.db.db_actions.insert_into_jobs') as mock_insert:

        mock_insert.return_value = None
        mock_publish.return_value = None

        response = await job_queue_services.add_job()

        assert response.message == "Job added"
        assert response.jobId is not None

@pytest.mark.asyncio
async def test_get_status():
    with mock.patch('app.db.db_actions.find_jobs') as mock_find_jobs, \
         mock.patch('app.db.db_actions.find_jobs_by_status') as mock_find_jobs_by_status:
        
        mock_job = Job(id="test_id", timestamp="2021-01-01T00:00:00")
        mock_find_jobs.return_value = [mock_job] * 10  # Return a list of 10 mock jobs
        mock_find_jobs_by_status.return_value = [mock_job] * 10

        response = await job_queue_services.get_status(10, None)

        assert response.message == "Retrieved latest jobs"
        assert len(response.data.jobs) == 10  # Expecting 10 jobs in the response
