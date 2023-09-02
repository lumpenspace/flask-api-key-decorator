# test_require_api_key.py

import pytest
from flask import Flask
from flask_api_key_decorator import require_api_key

def test_require_api_key():
    app = Flask(__name__)

    @app.route('/')
    @require_api_key
    def home():
        return "Hello, World!"

    test_client = app.test_client()

    # Test without API key
    response = test_client.get('/')
    assert response.status_code == 403
    assert response.get_json() == {"message": "Invalid API key"}

    # Test with invalid API key
    response = test_client.get('/', headers={'x-api-key': 'invalid_key'})
    assert response.status_code == 403
    assert response.get_json() == {"message": "Invalid API key"}

    # Test with valid API key
    app.config['API_KEY'] = 'valid_key'
    response = test_client.get('/', headers={'x-api-key': 'valid_key'})
    assert response.status_code == 200
    assert response.data.decode() == "Hello, World!"