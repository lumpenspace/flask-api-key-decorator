# Flask API Key Decorator

A simple decorator for requiring an API key in order to access flask endpoints or methods.

## Installation

```bash
pip install flask-api-key-decorator
```

## Usage

Include the decorator in your project:

```python
from flask import Flask
from flask_api_key_decorator import require_api_key
```

Use it on a route:

```python
@app.route('/')
@require_api_key
def home():
    return "Hello, World!"

```

... or on a method:

```python
class Home(Resource):
    @require_api_key
    def get(self):
        return "Hello, World!"
```
