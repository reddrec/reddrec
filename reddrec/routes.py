from flask import Blueprint, jsonify, make_response, render_template
from .jobs import process_job, JobStatus
from .validation import valid_username

bp = Blueprint('routes', __name__)

@bp.route('/recommend/<username>')
def recommend(username):
    """
    Accept a new request for recommendations.
    Enqueues job if username is not in cache.

    Responses (all json):
    - 202 (accepted)
    - 200 (cache hit)
    - 400 (bad request: invalid username)
    - 404 (Reddit user not found)
    - 500 (server error: job failed)
    """

    # Our system expects lowercased usernames.
    # Reddit usernames are case-insensitive, anyways.
    username = username.lower()

    if not valid_username(username):
        return jsonify(error='Invalid Reddit username.'), 400

    # Perform async job processing or get cached recommendations.
    job = process_job(username)

    if job.status is JobStatus.COMPLETED:
        # Don't use jsonify here since job.data is already a json string
        response = make_response(job.data, 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    elif job.status is JobStatus.PROCESSING:
        return jsonify(status='Fetching your recommendations.'), 202

    elif job.status is JobStatus.FAILED_CANNOT_RECOMMEND_USER:
        return jsonify(error='We can\'t find enough data for that Redditor.'), 404

    return jsonify(error='Job failed, please try again later.'), 500
