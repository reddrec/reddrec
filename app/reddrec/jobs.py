from enum import Enum
from flask.json import dumps
from reddrec.recommender import recommend
from redis import Redis
from rq import Queue

# Store processed results for 6 hours
RESULTS_TTL = 6 * 60 * 60

redis_conn = Redis(host='redis', port=6379)
queue = Queue(connection=redis_conn)

class JobStatus(Enum):
    PROCESSING = 1
    COMPLETED = 2
    FAILED_UNKNOWN_CAUSE = 3
    FAILED_CANNOT_RECOMMEND_USER = 4

class Job:
    def __init__(self, status, data=None):
        self.status = status
        self.data = data

def job_id(username):
    """
    The id of the RQ job that is processing this user.
    Redis key becomes `rq:job:{job_id(username)}`.
    """

    return f'reddrec:recommend:{username.lower()}'

def result_key(username):
    """
    The key for cached recommendations of this user.
    """

    return f'reddrec:result:{username.lower()}'

def process_job(username):
    """
    Handles async job processing for given user.

    Returns a Job object.
    Completed jobs contain recommendation data.
    """

    cached = redis_conn.get(result_key(username))

    if cached:
        return Job(JobStatus.COMPLETED, cached)

    rq_job = queue.fetch_job(job_id(username))
    if not rq_job:
        rq_job = queue.enqueue(recommend, username, job_id=job_id(username))

    if rq_job.is_finished:
        if rq_job.result is None:
            rv = Job(JobStatus.FAILED_CANNOT_RECOMMEND_USER)
        else:
            # Convert job result to json and store it in Redis
            json = dumps(rq_job.result)
            redis_conn.setex(result_key(username), RESULTS_TTL, json)
            rv = Job(JobStatus.COMPLETED, json)

        # Finalize by deleting, preventing bugs due to race conditions
        rq_job.delete()
        return rv

    if rq_job.is_failed:
        # TODO: Log errors somewhere & maybe implement a retry policy
        rq_job.delete()
        return Job(JobStatus.FAILED_UNKNOWN_CAUSE)

    return Job(JobStatus.PROCESSING)
