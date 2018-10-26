import json
from flask import current_app, g
from llc1_document_api.config import PDF_GENERATION_API
from llc1_document_api.exceptions import ApplicationError
from llc1_document_api.dependencies.storage_api_service import StorageAPIService
from llc1_document_api.extensions import db


class PdfGenerationService(object):
    @staticmethod
    def generate_pdf(extents, reference_item):
        """Generates the llc1 PDF"""
        try:
            db.session.add(reference_item)
            db.session.flush()

            extents['referenceNumber'] = reference_item.id

            current_app.logger.info("Calling pdf-generation-api")

            response = g.requests.post(PDF_GENERATION_API,
                                       data=json.dumps(extents),
                                       headers={'X-Trace-ID': g.trace_id, 'Content-Type': 'application/json'})

            if response.status_code != 201:
                current_app.logger.exception('Failed to generate PDF. TraceID : {} - Status code:{}, message:{}'
                                             .format(g.trace_id,
                                                     response.status_code,
                                                     response.text))
                raise ApplicationError("Error generating PDF", "GEN-01", response.status_code)

            current_app.logger.info("pdf-generation-api responded with status: {}".format(response.status_code))

            pdf_api_response = response.json()

            response_obj = {
                "reference_number": reference_item.formatted_id(),
                "document_url": pdf_api_response["document_url"],
                "external_url": pdf_api_response["external_url"],
                "number_of_charges": len(pdf_api_response["included_charges"])
            }

            reference_item.document = pdf_api_response["document_url"]

            supporting_documents = {}

            for item in pdf_api_response['included_charges']:
                charge = item['item']
                if 'Light obstruction notice' in charge['charge-type']:
                    supporting_documents[item['display_id']] = PdfGenerationService.url_for_documents(
                        charge['documents-filed'])

            if supporting_documents:
                response_obj['supporting_documents'] = supporting_documents

            current_app.logger.info('Committing SearchItem with id: {}'.format(reference_item.id))
            db.session.commit()

            return response_obj

        except ApplicationError:
            current_app.logger.info('Rolling back SearchItem with id: {}'.format(reference_item.id))
            db.session.rollback()
            raise
        except Exception as ex:
            current_app.logger.exception('Failed to generate PDF. TraceID : {} - Exception :{}'.format(
                g.trace_id,
                ex))
            current_app.logger.info('Rolling back SearchItem with id: {}'.format(reference_item.id))
            db.session.rollback()

            raise ApplicationError("Error generating PDF", "GEN-02", 500)

    @staticmethod
    def url_for_documents(documents_filed):
        form_a = documents_filed['form-a'][0]

        return StorageAPIService.get_external_url(form_a["subdirectory"], form_a['bucket'])
