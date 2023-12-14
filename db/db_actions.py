from db.db_config import jobs_collection

def insert_into_jobs(job_dic: dict):
    try:
        jobs_collection.insert_one(job_dic)
    except Exception as e:
        raise Exception(str(e))

def find_jobs():
    try:
        jobs= jobs_collection.find({},{"_id":0})
    except Exception as e:
        raise Exception(str(e))
    return jobs

def find_jobs_by_status(status:str):
    try:
        jobs= jobs_collection.find({"status":status},{"_id":0})
    except Exception as e:
        raise Exception(str(e))
    return jobs


def find_job_by_id(job_id:str):
    try:
        jobs = find_jobs()
    except Exception as e:
        raise Exception(str(e))
    
    for job in jobs:
        if job["id"]==job_id:
            return job
    return None


def update_job(job_id:str,
               job:dict):
    try:
        jobs_collection.update_one({"id": job_id}, {"$set": job})
    except Exception as e:
        raise Exception(str(e))