import sys
print(sys.path)
import pytest
from flask import Flask
from require_api_key import require_api_key

def test_require_api_key(monkeypatch):
    app = Flask(__name__)
    monkeypatch.setenv('API_KEY', 'valid_key')

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
    response = test_client.get('/', headers={'x-api-key': 'valid_key'})
    assert response.status_code == 200
    assert response.data.decode() == "Hello, World!"
  
def test_require_api_key_with_custom_header(monkeypatch):
    app = Flask(__name__)
    monkeypatch.setenv('API_KEY', 'valid_key')

    @app.route('/')
    @require_api_key(header_name='custom-header')
    def home():
      return "Hello, World!"

    test_client = app.test_client()

    # Test with no api key
    response = test_client.get('/')
    assert response.status_code == 403
    assert response.get_json() == {"message": "Invalid API key"}

    # Test with invalid API key
    response = test_client.get('/', headers={'custom-header': 'valid_key'})
    assert response.status_code == 200
    assert response.data.decode() == "Hello, World!"

def test_require_api_key_without_setting_key(monkeypatch):
    app = Flask(__name__)

    test_client = app.test_client()

    # Test without setting API key
    monkeypatch.delenv('API_KEY', raising=False)
    with pytest.raises(ValueError) as exc_info:
        @app.route('/')
        @require_api_key
        def home():
            return "Hello, World!"
        test_client.get('/')

    assert (str(exc_info.value)) == 'API key is not set'
