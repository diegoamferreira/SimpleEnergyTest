from unittest import TestCase

import requests
import responses

from errors.simple_energy_errors import ResposeStatusCodeError
from parse_data.parse_files_list import ParseFilesList
from tests.test_datas.html_contents_raw import FILE_LIST_PAGE_HTML, EMPTY_FILE_LIST_PAGE_HTML


# https://github.com/getsentry/responses#basics


class TestParseFilesList(TestCase):

    def test_files_list_erro_status_code_diferente_200(self):
        """
        Verifica se teremos o erro quando o status code da resposta for diferente de 200
         """
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                'https://simpleenergy.com.br/teste/',
                body=FILE_LIST_PAGE_HTML,
                status=204,
                content_type="text/html; charset=UTF-8",
            )
            resp = requests.post('https://simpleenergy.com.br/teste/')
            with self.assertRaises(ResposeStatusCodeError) as context:
                file_list = ParseFilesList(response=resp).parse()

    def test_files_list_nenhum_boleto_na_pagina(self):
        """
        Verifica se teremos o retorno esperado quando nenhum boleto for encontrado na página
         """
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                'https://simpleenergy.com.br/teste/',
                body=EMPTY_FILE_LIST_PAGE_HTML,
                status=200,
                content_type="text/html; charset=UTF-8",
            )
            resp = requests.post('https://simpleenergy.com.br/teste/')
            file_list = ParseFilesList(response=resp).parse()
            self.assertEqual(file_list, [])

    def test_files_list_formato_dados_boletos_como_esperado(self):
        """
        Verifica se teremos o retorno esperado quando nenhum boleto for encontrado na página
         """
        self.maxDiff = None
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                'https://simpleenergy.com.br/teste/',
                body=FILE_LIST_PAGE_HTML,
                status=200,
                content_type="text/html; charset=UTF-8",
            )
            resp = requests.post('https://simpleenergy.com.br/teste/')
            file_list = ParseFilesList(response=resp).parse()
            file_list_valid = [
                {'client_code': 98465, 'arquivo': 'Arquivo 1', 'href': 'arquivo1-98465.txt', 'nome': 'arquivo.txt'},
                {'client_code': 98465, 'arquivo': 'Arquivo 1', 'href': 'arquivo1-98465.pdf', 'nome': 'arquivo.pdf'},
                {'client_code': 98465, 'arquivo': 'Arquivo 2', 'href': 'arquivo2-98465.txt', 'nome': 'arquivo2.txt'},
                {'client_code': 98465, 'arquivo': 'Arquivo 2', 'href': 'arquivo2-98465.pdf', 'nome': 'arquivo2.pdf'}
            ]
            self.assertEqual(file_list, file_list_valid)
