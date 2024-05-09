import os
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult

from ms_ai_code_academy import settings
from ms_ai_code_academy.ms_ai_document_intelligence.bounty_ledger.invoice import Invoice

# configure logging
import logging
from logging.config import dictConfig
dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger(__name__)

load_dotenv()


class BountyLedger:

    def __init__(self, file_path: str, content_type: str = 'application/pdf'):
        """
        :param file_path: the path to the invoice to be processed
        :param content_type: the content type of the invoice
        """
        self.document_intelligence_client = DocumentIntelligenceClient(endpoint=os.getenv('AZURE_AI_SERVICE_ENDPOINT'),
                                                                       credential=AzureKeyCredential(os.getenv('AZURE_AI_SERVICE_KEY')))
        with open(file_path, 'rb') as f:
            self.analyzer = self.document_intelligence_client.begin_analyze_document(model_id='prebuilt-invoice',
                                                                                     analyze_request=f,
                                                                                     content_type=content_type)

    def process_invoices(self) -> Invoice:
        """
        :return: an invoice object with the necessary information
        """
        # get the results from executing the analyzer
        invoices_result: AnalyzeResult = self.analyzer.result()
        logger.debug(f'Invoices analysis result: {invoices_result}')
        # process the "documents" in the result
        if invoices_result.documents:
            logger.debug(f'Invoice analysis extracted {len(invoices_result.documents)} document(s)')
            for idx, invoice in enumerate(invoices_result.documents):
                vendor_name = invoice.fields.get('VendorName')
                if vendor_name:
                    vendor_name = vendor_name.get('content').title()
                logger.debug(f'Invoice vendor name: {vendor_name}')
                customer_name = invoice.fields.get('CustomerName')
                if customer_name:
                    customer_name = customer_name.get('content').title()
                logger.debug(f'Invoice customer name: {customer_name}')
                amount = invoice.fields.get('InvoiceTotal')
                if amount:
                    amount = amount.get('content')
                logger.debug(f'Invoice amount: {amount}')
                if vendor_name and customer_name and amount:
                    return Invoice(vendor_name=vendor_name, customer_name=customer_name, amount=amount)


if __name__ == '__main__':
    # initialize the ledger object
    ledger = BountyLedger('D:\codebase\ms-ai-code-academy\data\samples\invoice.pdf')
    # analyze the invoice
    invoice = ledger.process_invoices()
    logger.info(f'Extracted invoice data: {invoice}')
