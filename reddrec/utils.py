def is_flask_in_testing_mode():
    """
    Long name to ensure we don't call this function outside of a Flask context.
    (e.g. don't call it from an rq job)
    """
    from flask import current_app
    return bool(current_app.config.get('testing'))
