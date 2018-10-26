from unittest import TestCase
from unittest.mock import patch, MagicMock
from llc1_document_api.dependencies.pdf_generation_service import PdfGenerationService
from llc1_document_api import main
from flask import g
from llc1_document_api.exceptions import ApplicationError
from llc1_document_api.models import SearchItem

mock_lon = {
    "display_id": "LLC-0",
    "item": {
        "charge-type": "Light obstruction notice",
        "documents-filed": {
            "form-a": [
                {
                    "bucket": "lon",
                    "subdirectory": "123"
                }
            ]
        }
    }
}


class TestPdfGenerationService(TestCase):

    @patch('llc1_document_api.dependencies.pdf_generation_service.db')
    @patch('llc1_document_api.dependencies.pdf_generation_service.PDF_GENERATION_API')
    def test_successful_response(self, mock_config, mock_db):
        with main.app.test_request_context():
            g.trace_id = "test_id"
            g.requests = MagicMock()
            mock_config.return_value = "abc"
            g.requests.post.return_value.status_code = 201
            g.requests.post.return_value.json.return_value = {"document_url": "abc123",
                                                              "included_charges": [],
                                                              "external_url": "abc"}

            mock_reference_item = SearchItem(MagicMock(), "", "")
            mock_reference_item.id = 12

            result = PdfGenerationService.generate_pdf({"things": "ABC"}, mock_reference_item)
            expected_result = {
                'reference_number': '000 000 012',
                'document_url': 'abc123',
                'external_url': 'abc',
                'number_of_charges': 0
            }
            self.assertEqual(result, expected_result)
            self.assertEqual(mock_reference_item.document, expected_result['document_url'])
            mock_db.session.add.assert_called(mock_reference_item)
            mock_db.session.commit.assert_called()

    @patch('llc1_document_api.dependencies.pdf_generation_service.StorageAPIService')
    @patch('llc1_document_api.dependencies.pdf_generation_service.db')
    @patch('llc1_document_api.dependencies.pdf_generation_service.PDF_GENERATION_API')
    def test_successful_response_including_lons(self, mock_config, mock_db, mock_storage_api):
        with main.app.test_request_context():
            g.trace_id = "test_id"
            g.requests = MagicMock()
            mock_config.return_value = "abc"
            mock_storage_api.get_external_url.return_value = 'lons-external-url'
            g.requests.post.return_value.status_code = 201
            g.requests.post.return_value.json.return_value = {"document_url": "abc123",
                                                              "included_charges": [mock_lon],
                                                              "external_url": "abc"}

            mock_reference_item = SearchItem(MagicMock(), "", "")
            mock_reference_item.id = 12

            result = PdfGenerationService.generate_pdf({"things": "ABC"}, mock_reference_item)

            expected_result = {
                'reference_number': '000 000 012',
                'document_url': 'abc123',
                'supporting_documents': {
                    'LLC-0': 'lons-external-url'
                },
                "external_url": "abc",
                'number_of_charges': 1
            }
            self.assertEqual(result, expected_result)
            mock_db.session.add.assert_called(mock_reference_item)
            mock_db.session.commit.assert_called()

    @patch('llc1_document_api.dependencies.pdf_generation_service.db')
    @patch('llc1_document_api.dependencies.pdf_generation_service.current_app')
    @patch('llc1_document_api.dependencies.pdf_generation_service.PDF_GENERATION_API')
    def test_unsuccessful_response(self, mock_config, mock_app, mock_db):
        with main.app.test_request_context():
            g.trace_id = "test_id"
            g.requests = MagicMock()
            mock_config.return_value = "abc"
            g.requests.post.return_value.status_code = 400
            g.requests.post.return_value.text = "test-error"

            mock_reference_item = SearchItem(MagicMock(), "", "")
            mock_reference_item.id = 12

            try:
                PdfGenerationService.generate_pdf({"things": "ABC"}, mock_reference_item)
                self.fail("Exception should have been thrown")
            except ApplicationError as ex:
                self.assertEqual(ex.code, "GEN-01")
                self.assertEqual(ex.message, "Error generating PDF")
                self.assertEqual(ex.http_code, 400)
                mock_db.session.add.assert_called(mock_reference_item)
                mock_db.session.rollback.assert_called()
                mock_app.logger.exception.assert_called()
                mock_app.logger.exception.assert_called_with(
                    'Failed to generate PDF. TraceID : test_id - Status code:400, message:test-error')

    @patch('llc1_document_api.dependencies.pdf_generation_service.db')
    @patch('llc1_document_api.dependencies.pdf_generation_service.current_app')
    @patch('llc1_document_api.dependencies.pdf_generation_service.PDF_GENERATION_API')
    def test_exception_response(self, mock_config, mock_app, mock_db):
        with main.app.test_request_context():
            g.trace_id = "test_id"
            g.requests = MagicMock()
            g.requests.post.side_effect = Exception('test exception')
            mock_config.return_value = "abc"

            mock_reference_item = SearchItem(MagicMock(), "", "")
            mock_reference_item.id = 12

            try:
                PdfGenerationService.generate_pdf({"things": "ABC"}, mock_reference_item)
                self.fail("Exception should have been thrown")
            except ApplicationError as ex:
                self.assertEqual(ex.code, "GEN-02")
                self.assertEqual(ex.message, "Error generating PDF")
                self.assertEqual(ex.http_code, 500)
                mock_db.session.add.assert_called(mock_reference_item)
                mock_db.session.rollback.assert_called()
                mock_app.logger.exception.assert_called()
                mock_app.logger.exception.assert_called_with(
                    'Failed to generate PDF. TraceID : test_id - Exception :test exception')
