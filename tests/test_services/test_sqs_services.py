import pytest
from unittest import mock
from services import sqs_services  # Adjusted import statement
from db.models.JobQueue import JobStatus
from unittest.mock import MagicMock
from unittest.mock import patch
import app.services.sqs_services as sqs_services_module
import json


def test_get_queue_attributes():
    # Define the expected mock response
    expected_response = {
        'Attributes': {
            'ApproximateNumberOfMessages': '10',
            'ApproximateNumberOfMessagesNotVisible': '5',
            'ApproximateNumberOfMessagesDelayed': '2'
        }
    }

    # Patch the 'sqs.get_queue_attributes' method
    with patch.object(sqs_services_module.sqs, 'get_queue_attributes', return_value=expected_response) as mock_get_attributes:
        # Call the function
        attributes = sqs_services_module.get_queue_attributes()

        # Assertions
        assert attributes['Attributes']['ApproximateNumberOfMessages'] == '10'
        assert attributes['Attributes']['ApproximateNumberOfMessagesNotVisible'] == '5'
        assert attributes['Attributes']['ApproximateNumberOfMessagesDelayed'] == '2'
        
        # Check if the mock was called with expected arguments
        mock_get_attributes.assert_called_once_with(
            QueueUrl=sqs_services_module.queue_url,
            AttributeNames=['ApproximateNumberOfMessages', 'ApproximateNumberOfMessagesNotVisible', 'ApproximateNumberOfMessagesDelayed']
        )

def test_process_job():
    job_id = "test_job_id"
    mock_job = {"id": job_id, "numberOfAttempts": 0, "status": ""}

    with mock.patch('services.sqs_services.requests.post', return_value=mock.Mock(status_code=200)) as mock_requests_post, \
         mock.patch('db.db_actions.find_job_by_id', return_value=mock_job) as mock_find_job_by_id, \
         mock.patch('db.db_actions.update_job') as mock_update_job, \
         mock.patch('services.sqs_services.publish_job') as mock_publish_job:

        sqs_services.process_job(job_id)

        mock_find_job_by_id.assert_called_once_with(job_id)
        mock_requests_post.assert_called_once()
        mock_update_job.assert_called_once()
        mock_publish_job.assert_not_called()

        # Test failure scenario
        mock_requests_post.return_value = mock.Mock(status_code=500)
        sqs_services.process_job(job_id)

        # Check if the job is retried
        assert mock_publish_job.call_count == 1