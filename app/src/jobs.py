from enum import Enum
from redis import Redis
from rq import Queue

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
    from flask import jsonify
    import random

    fake_data = {
        "username": username,
        "recommendations": [
            {"subreddit": "xbox", "confidence": random.random()},
            {"subreddit": "ps4",  "confidence": random.random()},
            {"subreddit": "pc",   "confidence": random.random()},
        ]
    }

    return Job(JobStatus.COMPLETED, fake_data)
