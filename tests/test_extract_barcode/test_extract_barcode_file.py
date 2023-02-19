from unittest import TestCase

import requests
import responses

from errors.simple_energy_errors import ResposeStatusCodeError
from src.extract_file.extract_barcode_file import ExtractBarcodeFile


class TestExtractBarcodeFile(TestCase):

    def test_extract_barcode_erro_status_code_diferente_200(self):
        """
        Verifica se teremos o erro quando o status code da resposta for diferente de 200
         """
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                'https://simpleenergy.com.br/teste/arquivo1-321465.pdf',
                body="{}",
                status=204,
                content_type="'Content-Type': 'application/pdf'",
            )
            resp = requests.get('https://simpleenergy.com.br/teste/arquivo1-321465.pdf')
            with self.assertRaises(ResposeStatusCodeError):
                barcode_extractor = ExtractBarcodeFile(response=resp)

    def test_extract_barcode_filetype_esperado(self):
        """
        Verifica se o tipo de arquivo vai ser o esperado.
         """
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                'https://simpleenergy.com.br/teste/arquivo1-321465.pdf',
                body="{}",
                status=200,
                content_type="'Content-Type': 'application/pdf'",
            )
            rsps.add(
                responses.GET,
                'https://simpleenergy.com.br/teste/arquivo1-321465.txt',
                body="{}",
                status=200,
                content_type="'Content-Type': 'text/plain'",
            )
            resp_pdf = requests.get('https://simpleenergy.com.br/teste/arquivo1-321465.pdf')
            barcode_extractor_pdf = ExtractBarcodeFile(response=resp_pdf)
            self.assertEqual(barcode_extractor_pdf.filetype, 'pdf')

            resp_txt = requests.get('https://simpleenergy.com.br/teste/arquivo1-321465.txt')
            barcode_extractor_txt = ExtractBarcodeFile(response=resp_txt)
            self.assertEqual(barcode_extractor_txt.filetype, 'txt')

    def test_extract_barcode_from_txt_response(self):
        """
        Verifica se a resposta da extração do codigo do boleto bate com o esperado
        """
        with open("tests/test_datas/arquivo1-321465.txt", "r") as file:
            file_txt = file.read()
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                'https://simpleenergy.com.br/teste/arquivo1-321465.txt',
                body=file_txt,
                status=200,
                content_type="'Content-Type': 'text/plain'",
            )
            resp_txt = requests.get('https://simpleenergy.com.br/teste/arquivo1-321465.txt')
            barcode_extractor = ExtractBarcodeFile(response=resp_txt)
            barcode = barcode_extractor.execute()
            self.assertEqual(barcode, 'e793ff53f0ca92f6205bc871546a2c79e54c4e0cd42c6a191e45e771d7217aca')

    def test_extract_barcode_from_pdf_response(self):
        """
        Verifica se a resposta da extração do codigo do boleto bate com o esperado
        """
        with open("tests/test_datas/arquivo1-321465.pdf", "rb") as file:
            file_pdf = file.read()
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                'https://simpleenergy.com.br/teste/arquivo1-321465.pdf',
                body=file_pdf,
                status=200,
                content_type="'Content-Type': 'application/pdf'",
            )
            resp_txt = requests.get('https://simpleenergy.com.br/teste/arquivo1-321465.pdf')
            barcode_extractor = ExtractBarcodeFile(response=resp_txt)
            barcode = barcode_extractor.execute()
            self.assertEqual(barcode, 'e793ff53f0ca92f6205bc871546a2c79e54c4e0cd42c6a191e45e771d7217aca')
