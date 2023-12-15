from fastapi.testclient import TestClient
from unittest import mock
from main import app

client = TestClient(app)

def test_add_job_route():
    with mock.patch('app.services.job_queue_services.add_job') as mock_add_job:
        mock_add_job.return_value = {"message": "Job added", "jobId": "test_id"}
        response = client.post("/addJob")

        assert response.status_code == 200
        assert "message" in response.json()
        assert "jobId" in response.json()
        assert response.json()["message"] == "Job added"


def test_get_status_route():
    with mock.patch('app.services.job_queue_services.get_status') as mock_get_status:
        mock_get_status.return_value = {"message": "Retrieved latest jobs", "data": {"jobs": [], "total_jobs_returned": 0}}
        response = client.get("/status?count=10")

        assert response.status_code == 200
        assert "message" in response.json()
        assert "data" in response.json()
        assert response.json()["message"] == "Retrieved latest jobs"
