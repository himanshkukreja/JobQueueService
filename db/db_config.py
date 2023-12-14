from pymongo import MongoClient
from config.secrets_config import db_url


# MongoDB setup
client = MongoClient(db_url)
db = client.job_queue_system
jobs_collection = db.jobs
