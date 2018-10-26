from llc1_document_api import main
from flask_testing import TestCase
from unittest.mock import patch
from llc1_document_api.exceptions import ApplicationError


class TestExceptions(TestCase):

    def create_app(self):
        return main.app

    @patch('llc1_document_api.exceptions.current_app')
    def test_application_error_init_default_http_code(self, mock_app):
        error = ApplicationError("test message", "abc")

        self.assertEqual(error.message, "test message")
        self.assertEqual(error.code, "abc")
        self.assertEqual(error.http_code, 500)

    @patch('llc1_document_api.exceptions.current_app')
    def test_application_error_init_set_http_code(self, mock_app):
        error = ApplicationError("test message", "abc", 400)

        self.assertEqual(error.message, "test message")
        self.assertEqual(error.code, "abc")
        self.assertEqual(error.http_code, 400)

    @patch('llc1_document_api.app.validate')
    @patch('llc1_document_api.exceptions.current_app')
    def test_exception_handler(self, mock_app, validate):

        @main.app.route("/test-error")
        def test_error():
            raise ApplicationError("test message", "abc")

        response = self.client.get('/test-error', headers={'Authorization': 'x'})

        self.assert_status(response, 500)

    @patch('llc1_document_api.app.validate')
    @patch('llc1_document_api.exceptions.current_app')
    def test_exception_handler_400(self, mock_app, validate):

        @main.app.route("/test-error-400")
        def test_error_400():
            raise ApplicationError("test message", "abc", 400)

        response = self.client.get('/test-error-400', headers={'Authorization': 'x'})

        self.assert_status(response, 400)

    @patch('llc1_document_api.app.validate')
    @patch('llc1_document_api.exceptions.current_app')
    def test_exception_handler_unhandled(self, mock_app, validate):

        @main.app.route("/test-error-unhandled")
        def test_error_unhandled():
            raise Exception("test message")

        response = self.client.get('/test-error-unhandled', headers={'Authorization': 'x'})

        self.assert_status(response, 500)
