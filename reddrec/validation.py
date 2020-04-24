import re

VALID_USER_REGEXP = re.compile('[a-zA-Z\\-_\\d]+')

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
