from enum import Enum
from redis import Redis
from rq import Queue
from flask.json import dumps

redis_conn = Redis(host='redis', port=6379)
q = Queue(connection=redis_conn)

class JobStatus(Enum):
    PROCESSING = 1
    COMPLETED = 2
    FAILED_UNKNOWN_CAUSE = 3
    FAILED_USER_NOT_FOUND = 4

class Job:
    def __init__(self, status, data=None):
        self.status = status
        self.data = data

def process_job(username):
    """
    Handles async job processing for given user.

    Returns a Job object.
    Completed jobs contain recommendation data.
    """

    cached = redis_conn.get(f"cached-response:{username}")

    if cached:
        return Job(JobStatus.COMPLETED, cached)

    status, rq_job = rq_request_job(username)

    if status is JobStatus.COMPLETED:

        # Convert job result to json and enqueue it in cache
        json = dumps(rq_job.result)
        redis_conn.put(f"cached-response:{username}", json)
        return Job(JobStatus.COMPLETED, json)

    return Job(status)

def rq_request_job(username):
    job = q.fetch_job(username)
    return JobStatus.PROCESSING, job

def fake_rq_request_job(username):
    import random

    fake_data = {
        "username": username,
        "recommendations": [
            {"subreddit": "xbox", "confidence": random.random()},
            {"subreddit": "ps4",  "confidence": random.random()},
            {"subreddit": "pc",   "confidence": random.random()},
        ]
    }

    class FakeResp:
        def __init__(data):
            self.result=data

    return JobStatus.COMPLETED, FakeResp(fake_data)
