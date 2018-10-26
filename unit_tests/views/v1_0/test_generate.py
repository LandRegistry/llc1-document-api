from llc1_document_api import main
from flask import url_for
from flask_testing import TestCase
from unittest.mock import patch
import json


class TestGenerate(TestCase):

    def create_app(self):
        return main.app

    @patch('llc1_document_api.views.v1_0.generate.current_app')
    @patch('llc1_document_api.app.validate')
    @patch('llc1_document_api.views.v1_0.generate.PdfGenerationService')
    @patch('llc1_document_api.views.v1_0.generate.PayloadValidator')
    def test_generate_llc1_with_valid_input(self, extent_validator_mock, mock_pdf_service, validate, mock_current_app):
        """should respond with a 201 and return the expected url if input validation succeeds."""
        expected_response = {
            'document_url': 'http://storage-api/llc1/1234'
        }

        extent_validator_mock.validate.return_value = True
        mock_pdf_service.generate_pdf.return_value = expected_response

        response = self.client.post(url_for('generate.generate_llc1'),
                                    data=json.dumps({"source": "LLC1 Unit Test"}),
                                    content_type="application/json",
                                    headers={'Authorization': 'Fake JWT'})
        response_json = json.loads(response.get_data(as_text=True))
        self.assert_status(response, 201)
        mock_current_app.logger.performance_platform.assert_called_with(
            "Successfully generated PDF"
        )
        self.assertEqual(response_json, expected_response)

    @patch('llc1_document_api.views.v1_0.generate.current_app')
    @patch('llc1_document_api.app.validate')
    @patch('llc1_document_api.views.v1_0.generate.PdfGenerationService')
    @patch('llc1_document_api.views.v1_0.generate.PayloadValidator')
    def test_generate_valid_llc1_including_lons(
        self, extent_validator_mock, mock_pdf_service, validate, mock_current_app
    ):
        """should respond with a 201 and return the expected url if input validation succeeds."""
        expected_response = {
            'document_url': 'http://storage-api/llc1/1234',
            'supporting_documents': {
                'LLC-2': 'link/to/zip'
            }
        }

        extent_validator_mock.validate.return_value = True
        mock_pdf_service.generate_pdf.return_value = expected_response

        response = self.client.post(url_for('generate.generate_llc1'),
                                    data=json.dumps({"source": "LLC1 Unit Test"}),
                                    content_type="application/json",
                                    headers={'Authorization': 'Fake JWT'})
        response_json = json.loads(response.get_data(as_text=True))
        self.assert_status(response, 201)
        mock_current_app.logger.performance_platform.assert_called_with(
            "Successfully generated PDF"
        )
        self.assertEqual(response_json, expected_response)

    @patch('llc1_document_api.views.v1_0.generate.current_app')
    @patch('llc1_document_api.app.validate')
    @patch('llc1_document_api.views.v1_0.generate.PayloadValidator')
    def test_generate_llc1_with_invalid_input(self, extent_validator_mock, validate, mock_current_app):
        """should respond with a 400 if input validation fails."""
        extent_validator_mock.validate.return_value = False

        response = self.client.post(url_for('generate.generate_llc1'),
                                    headers={'Authorization': 'Fake JWT'})

        self.assert_status(response, 400)
        self.assertEqual(mock_current_app.logger.performance_platform.mock_calls, [])
