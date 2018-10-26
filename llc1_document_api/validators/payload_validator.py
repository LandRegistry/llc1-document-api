import simplejson as json

from jsonschema import validate
from llc1_document_api.schema.extents import PAYLOAD_SCHEMA


class PayloadValidator(object):

    @staticmethod
    def validate(extents):
        """Returns true if the given extents are valid. False otherwise."""
        try:
            json_ = json.loads(extents)
            validate(json_, PAYLOAD_SCHEMA)
            return True
        except Exception:
            return False
