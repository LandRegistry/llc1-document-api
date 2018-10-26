from llc1_document_api.extensions import db


class SearchItem(db.Model):
    __tablename__ = 'document_reference'

    id = db.Column(db.BigInteger, primary_key=True)
    date_of_search = db.Column(db.Date)
    document = db.Column(db.String)
    source = db.Column(db.String)

    def __init__(self, date_of_search, source, document=None):
        self.date_of_search = date_of_search
        self.source = source
        self.document = document

    def formatted_id(self):
        padded_id = '{}'.format(self.id).zfill(9)
        formatted_id = ' '.join(padded_id[i:i + 3] for i in range(0, len(padded_id), 3))
        # Limiting to 11 characters (9 for reference number + 3 spaces)
        return formatted_id[:11]
