from unittest import TestCase
from datetime import datetime
from llc1_document_api.models import SearchItem


class TestModels(TestCase):

    def test_search_item_init(self):
        date = datetime.now()
        source = "source"
        search_item = SearchItem(date, source)

        self.assertEqual(search_item.date_of_search, date)
        self.assertEqual(search_item.source, source)
        self.assertIsNone(search_item.document)

    def test_search_item_init_with_document_url(self):
        date = datetime.now()
        source = "source"
        document_location = 'some.location'

        search_item = SearchItem(date, source, document_location)

        self.assertEqual(search_item.date_of_search, date)
        self.assertEqual(search_item.source, source)
        self.assertEqual(search_item.document, document_location)

    def test_search_item_get_formatted_id(self):
        search_item = SearchItem(datetime.now(), "")
        search_item.id = 1

        formatted_id = search_item.formatted_id()
        expected = "000 000 001"
        self.assertEqual(formatted_id, expected)

        search_item.id = 999999999
        formatted_id = search_item.formatted_id()
        expected = "999 999 999"
        self.assertEqual(formatted_id, expected)

        search_item.id = 9999999999
        formatted_id = search_item.formatted_id()
        expected = "999 999 999"
        self.assertEqual(formatted_id, expected)
