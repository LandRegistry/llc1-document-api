from flask import Flask, g, request
from llc1_document_api.exceptions import ApplicationError
from jwt_validation.validate import validate
from jwt_validation.exceptions import ValidationFailure
import uuid
import requests

app = Flask(__name__)

app.config.from_pyfile("config.py")


@app.before_request
def before_request():
    g.trace_id = request.headers.get('X-Trace-ID', uuid.uuid4().hex)
    g.requests = requests.Session()
    g.requests.headers.update({'X-Trace-ID': g.trace_id})

    if '/health' in request.path:
        return

    if 'Authorization' not in request.headers:
        raise ApplicationError("Missing Authorization header", "AUTH1", 401)

    try:
        validate(app.config['AUTHENTICATION_API_URL'] + '/authentication/validate',
                 request.headers['Authorization'], g.requests)
    except ValidationFailure as fail:
        raise ApplicationError(fail.message, "AUTH1", 401)

    bearer_jwt = request.headers['Authorization']
    g.requests.headers.update({'Authorization': bearer_jwt})


@app.after_request
def after_request(response):
    response.headers["X-API-Version"] = "1.0.0"
    return response
