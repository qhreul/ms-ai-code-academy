import os
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult

from ms_ai_code_academy import settings
from ms_ai_code_academy.ms_ai_document_intelligence.cantina_credits.tax_form import Person, TaxForm

# configure logging
import logging
from logging.config import dictConfig
dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger(__name__)

load_dotenv()


class CantinaCredit:

    def __init__(self, file_path: str, content_type: str = 'application/pdf'):
        """
        :param file_path: the path to the invoice to be processed
        :param content_type: the content type of the invoice
        """
        self.document_intelligence_client = DocumentIntelligenceClient(endpoint=os.getenv('AZURE_AI_SERVICE_ENDPOINT'),
                                                                       credential=AzureKeyCredential(os.getenv('AZURE_AI_SERVICE_KEY')))
        with open(file_path, 'rb') as f:
            self.analyzer = self.document_intelligence_client.begin_analyze_document(model_id='cantina_credits_composed',
                                                                                     analyze_request=f,
                                                                                     content_type=content_type)

    def process_tax_forms(self) -> TaxForm:
        """
        :return: an tax form object with the necessary information
        """
        # get the results from executing the analyzer
        tax_form_result: AnalyzeResult = self.analyzer.result()
        logger.debug(f'Invoices analysis result: {tax_form_result}')
        # process the "documents" in the result
        if tax_form_result.documents:
            logger.debug(f'Tax form analysis extracted {len(tax_form_result.documents)} document(s)')
            for idx, tax_form in enumerate(tax_form_result.documents):
                contributor_ssn = tax_form.fields.get('SSN')
                if contributor_ssn:
                    contributor_ssn = contributor_ssn.get('content').replace(' ', '')
                logger.debug(f'Tax form contributor ssn: {contributor_ssn}')
                contributor_first_name = tax_form.fields.get('FirstName')
                if contributor_first_name:
                    contributor_first_name = contributor_first_name.get('content').title()
                logger.debug(f'Tax form contributor first name: {contributor_first_name}')
                contributor_last_name = tax_form.fields.get('LastName')
                if contributor_last_name:
                    contributor_last_name = contributor_last_name.get('content').title()
                logger.debug(f'Tax form contributor last name: {contributor_last_name}')
                contributor_city = tax_form.fields.get('City')
                if contributor_city:
                    contributor_city = contributor_city.get('content')
                logger.debug(f'Tax form contributor city: {contributor_city}')
                contributor_state = tax_form.fields.get('State')
                if contributor_state:
                    contributor_state = contributor_state.get('content')
                logger.debug(f'Tax form contributor state: {contributor_state}')
                contributor = Person(ssn=contributor_ssn, first_name=contributor_first_name,
                                     last_name=contributor_last_name, city=contributor_city, state=contributor_state)
                return TaxForm(main_contributor=contributor, spouse=None, taxable_amount=None)


if __name__ == '__main__':
    # initialize the cantina credit object
    ledger = CantinaCredit(file_path='D:\codebase\ms-ai-code-academy\data\samples\/f1040.pdf')
    # analyze the tax form
    tax_form_data = ledger.process_tax_forms()
    logger.info(f'Extracted invoice data: {tax_form_data}')
