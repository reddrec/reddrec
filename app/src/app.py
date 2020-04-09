from flask import Flask, jsonify
import re
from jobs import process_job, JobStatus

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello recommender system!\nTODO: serve static assets'

@app.route('/recommend/<username>')
def recommend(username):
    """
    Accept a new request for recommendations.
    Enqueues job if username is not in cache.

    Response:
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
        return jsonify({
            "error": "Invalid Reddit username."
        }), 400

    # Perform async job processing or get cached recommendations.
    response = process_job(username)

    if response.status is JobStatus.COMPLETED:
        return jsonify(response.data), 200

    elif response.status is JobStatus.PROCESSING:
        return jsonify({
            "status": "Fetching your recommendations.",
        }), 202

    elif response.status is JobStatus.FAILED_USER_NOT_FOUND:
        return jsonify({
            "error": "We couldn't find that Redditor.",
        }), 404

    return jsonify({
        "error": "Job failed, please try again later.",
    }), 500


VALID_USER_REGEXP = re.compile('[a-z\\-_\\d]+')
def valid_username(username):
    """
    We only want to process valid Reddit usernames.
    Rules found at: https://www.reddit.com/register
    """

    if not (3 <= len(username) <= 20):
        return False

    if VALID_USER_REGEXP.fullmatch(username) is None:
        return False

    return True


if __name__ == '__main__':
    app.run()
