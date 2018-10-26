from unittest import TestCase
from unittest.mock import MagicMock
from llc1_document_api import main
from flask import g, current_app
from llc1_document_api.dependencies.storage_api_service import StorageAPIService
from llc1_document_api.exceptions import ApplicationError


class TestStorageApiService(TestCase):

    def test_get_external_url_successful(self):
        with main.app.test_request_context():
            g.trace_id = "test_id"
            g.requests = MagicMock()
            current_app.config['STORAGE_API'] = "http://test.com"

            g.requests.get.return_value.status_code = 200
            g.requests.get.return_value.json.return_value = {'external_reference': 'test-reference'}

            result = StorageAPIService.get_external_url('file', 'bucket')

            self.assertIsNotNone(result)
            self.assertEqual('test-reference', result)

    def test_get_external_url_successful_subdirs(self):
        with main.app.test_request_context():
            g.trace_id = "test_id"
            g.requests = MagicMock()
            current_app.config['STORAGE_API'] = "http://test.com"

            g.requests.get.return_value.status_code = 200
            g.requests.get.return_value.json.return_value = {'external_reference': 'test-reference'}

            result = StorageAPIService.get_external_url('file', 'bucket', 'dir')

            self.assertIsNotNone(result)
            self.assertEqual('test-reference', result)

    def test_get_external_url_404(self):
        with main.app.test_request_context():
            g.trace_id = "test_id"
            g.requests = MagicMock()
            current_app.config['STORAGE_API'] = "http://test.com"

            g.requests.get.return_value.status_code = 404

            result = StorageAPIService.get_external_url('file', 'bucket')

            self.assertIsNone(result)

    def test_get_external_url_500(self):
        with main.app.test_request_context():
            g.trace_id = "test_id"
            g.requests = MagicMock()
            current_app.config['STORAGE_API'] = "http://test.com"

            g.requests.get.return_value.status_code = 500

            self.assertRaises(ApplicationError, StorageAPIService.get_external_url, 'file', 'bucket')
