from unittest import TestCase
from unittest.mock import patch, Mock
from llc1_document_api import app
from llc1_document_api.exceptions import ApplicationError


class TestApp(TestCase):

    TRACE_ID = 'some trace id'
    X_API_Version = '1.0.0'

    @patch('llc1_document_api.app.validate')
    @patch('llc1_document_api.app.uuid')
    @patch('llc1_document_api.app.requests')
    @patch('llc1_document_api.app.request')
    @patch('llc1_document_api.app.g')
    def test_before_request(self, g_mock, request_mock, requests_mock, uuid_mock, validate):
        """Should set a uuid trace id, update the trace id on global, and assign the session to the global object."""
        request_mock.headers = {
            "X-Trace-ID": self.TRACE_ID,
            "Authorization": "Fake JWT"
        }

        session_mock = Mock()
        requests_mock.Session.return_value = session_mock

        app.before_request()

        self.assertEqual(g_mock.trace_id, self.TRACE_ID)
        self.assertEqual(g_mock.requests, session_mock)

        g_mock.requests.headers.update.assert_any_call({'Authorization': "Fake JWT"})
        g_mock.requests.headers.update.assert_any_call({'X-Trace-ID': self.TRACE_ID})

    def test_after_request(self):
        """Should set the X-API-Version to the expected value."""
        response_mock = Mock()
        response_mock.headers = {
            "X-API-Version": None
        }
        result = app.after_request(response_mock)

        self.assertEqual(result.headers["X-API-Version"], self.X_API_Version)

    @patch('llc1_document_api.app.validate')
    @patch('llc1_document_api.app.uuid')
    @patch('llc1_document_api.app.requests')
    @patch('llc1_document_api.app.request')
    @patch('llc1_document_api.app.g')
    def test_before_request_no_auth(self, g_mock, request_mock, requests_mock, uuid_mock, validate):
        """Should set a uuid trace id, update the trace id on global, and assign the session to the global object."""
        request_mock.headers = {
            "X-Trace-ID": self.TRACE_ID
        }

        session_mock = Mock()
        requests_mock.Session.return_value = session_mock

        with self.assertRaises(ApplicationError):
            app.before_request()
