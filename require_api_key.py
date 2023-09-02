from functools import wraps
from os import environ
from flask import request, jsonify

def require_api_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == environ.get('API_KEY'):
            return view_function(*args, **kwargs)
        else:
            return jsonify({"message": "Invalid API key"}), 403
    if not hasattr(decorated_function, '__apidoc__'):
        decorated_function.__apidoc__ = {}

    decorated_function.__apidoc__.setdefault('params', {})['x-api-key'] = {
        'description': 'API key for authorization',
        'in': 'header',
        'type': 'string',
        'required': 'true'
    }

    return decorated_function