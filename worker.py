import json
from services.sqs_services import sqs,queue_url
from services.sqs_services import get_queue_attributes, process_job
from logger.logging import get_logger

logger = get_logger(__name__)

logger.debug("Starting the worker Service")
print(' [*] Waiting for messages. To exit press CTRL+C')
while True:
    # Poll the queue
    messages = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=0
    )

    if 'Messages' in messages:
        for message in messages['Messages']:
            job_data = json.loads(message['Body'])
            job_id = job_data['job_id']
            print()
            print("---------------------------------------------------------------")
            logger.debug(f"Received job with id {job_id}")
            
            try:
                process_job(job_id)
            except Exception as e:
                raise Exception(e)
            
            # Delete the message from the queue
            logger.debug(f"Deleting the job from queue with jobId {job_id}")
            
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
            logger.debug(f"Number of messages in queue, {get_queue_attributes()['Attributes']['ApproximateNumberOfMessages']}")

