import boto3
import requests
from config.config import sqs_url
from logger.logging import get_logger
import json
from uuid import uuid4
from config.config import max_delay,processing_system_endpoint,sqs_url,max_attempts
from config.secrets_config import candidate_key
from db import db_actions
from db.models.JobQueue import JobStatus

logger = get_logger(__name__)


sqs = boto3.client('sqs')
queue_url = sqs_url


def publish_job(job_id):
    random_deduplication_id = str(uuid4())
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps({"job_id": job_id}),
        MessageGroupId='my-message-group-id',
        MessageDeduplicationId=job_id+random_deduplication_id
    )
    logger.debug(f"Job pushed with id: {job_id}")


def get_queue_attributes():
    attributes = sqs.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=['ApproximateNumberOfMessages', 'ApproximateNumberOfMessagesNotVisible', 'ApproximateNumberOfMessagesDelayed']
    )
    return attributes


def process_job(job_id):
    try:
        job = db_actions.find_job_by_id(job_id)
    except Exception as e:
        raise Exception(e)

    if not job:
        logger.error(f"Job with id {job_id} not found in the db")
        return
    job['numberOfAttempts'] += 1
    attempts = job["numberOfAttempts"]
    try:
        logger.debug(f"Making a POST call to the endpoint {processing_system_endpoint} with job_id {job_id}")
        response = requests.post(
            processing_system_endpoint,
            json={"processId": job_id, "maxDelay": max_delay},
            headers={"candidateKey": candidate_key}
        )

        if response.status_code == 200:
            logger.debug(f"Job with id {job_id} processed successfully with response 200")
            job['status'] = JobStatus.SUCCESS.value

        elif response.status_code == 500:
            logger.error(f"Job with id {job_id} failed with response 500")
            
            if attempts<=max_attempts:
                job['status'] = JobStatus.PENDING.value
                logger.debug(f"Retrying job with id {job_id}, attempt number {job['numberOfAttempts']} which is less than max_attempts")
                publish_job(job_id)
            
            else:
                logger.debug(f"Number attempts exceeds the max_attempts hence marking the job as failed")
                job['status'] = JobStatus.FAILED.value

        else:
            logger.error(f"Unexpected response {response.status_code} for job {job_id}")


    except Exception as e:
        logger.error(f"Error processing job {job_id}: {e}")
        if attempts<=max_attempts:
                job['status'] = JobStatus.PENDING.value
                logger.debug(f"Retrying job with id {job_id}, attempt number {job['numberOfAttempts']} which is less than max_attempts")
                publish_job(job_id)

        else:
            logger.debug(f"Number attempts exceeds the max_attempts hence marking the job as failed")
            job['status'] =JobStatus.FAILED.value
        
    finally:
        logger.debug(f"Updating job {job_id} in the database")
        try:
            db_actions.update_job(job_id,job)
        except Exception as e:
            raise Exception(e)

        