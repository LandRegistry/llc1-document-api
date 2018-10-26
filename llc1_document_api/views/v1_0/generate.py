from flask import Blueprint, Response, request, current_app
import json
from datetime import datetime
from llc1_document_api.validators.payload_validator import PayloadValidator
from llc1_document_api.exceptions import ApplicationError
from llc1_document_api.dependencies.pdf_generation_service import PdfGenerationService
from llc1_document_api.models import SearchItem

generate = Blueprint('generate', __name__, url_prefix='/v1.0')


@generate.route("/generate", methods=['POST'])
def generate_llc1():
    """Generates an LLC1 document from the given extents and returns the URL to it's location in the file store."""
    current_app.logger.info("Endpoint called, validating payload")

    if not PayloadValidator.validate(request.get_data()):
        raise ApplicationError('The request body was invalid', None, 400)

    current_app.logger.info("Payload validated, generating PDF")

    search_reference = SearchItem(datetime.now(), request.get_json().get('source'))
    pdf = PdfGenerationService.generate_pdf(request.get_json(), search_reference)

    # Add custom log level for performance platform logs
    current_app.logger.performance_platform("Successfully generated PDF")

    return Response(json.dumps(pdf), 201, mimetype="application/json")
