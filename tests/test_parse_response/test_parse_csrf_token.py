from unittest import TestCase

import requests
import responses

from errors.simple_energy_errors import ResposeStatusCodeError, InputCSRFError
from parse_data.parse_csrf_token import ParseCSRFToken
from tests.test_datas.html_contents_raw import FORM_PAGE_HTML


# https://github.com/getsentry/responses#basics


class TestParseCSRFToken(TestCase):

    def test_csrf_token_erro_status_code_diferente_200(self):
        """
        Verifica se teremos o erro quando o status code da resposta for diferente de 200
         """
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                'https://simpleenergy.com.br/teste/',
                body="{}",
                status=204,
                content_type="text/html; charset=UTF-8",
            )
            resp = requests.get('https://simpleenergy.com.br/teste/')
            with self.assertRaises(ResposeStatusCodeError) as context:
                csrf = ParseCSRFToken(response=resp).parse()

    def test_csrf_token_nao_existe(self):
        """
        Verifica se teremos o erro esperado quando o campo csrf não for encontrado
         """
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                'https://simpleenergy.com.br/teste/',
                body="{}",
                status=200,
                content_type="text/html; charset=UTF-8",
            )
            resp = requests.get('https://simpleenergy.com.br/teste/')
            with self.assertRaises(InputCSRFError) as context:
                csrf = ParseCSRFToken(response=resp).parse()

    def test_csrf_token_bate_com_valor_esperado(self):
        """
        Verifica se o valor devolvido pelo parse bate com o valor esperado
         """
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                'https://simpleenergy.com.br/teste/',
                body=FORM_PAGE_HTML,
                status=200,
                content_type="text/html; charset=UTF-8",
            )
            resp = requests.get('https://simpleenergy.com.br/teste/')
            csrf_valid = 'bee7aceb836fdbc198fb80a119135a74b0114746ed8d8a5166aabcb9360192f6'
            csrf_parsed = ParseCSRFToken(resp).parse()
            self.assertEqual(csrf_valid, csrf_parsed)
