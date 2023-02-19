from errors.simple_energy_errors import InputCSRFError
from src.parse_data.parse_response import ParseResponseSoup


class ParseCSRFToken(ParseResponseSoup):

    def parse(self) -> str:
        """
        Encontra o csrf na página e coleta seu valor.
        :return: csrf token str
        """
        # Pega o input com o valor do csrf
        input = self.soup.find("input", {"name": "csrf"})

        # Verifica se o input foi encontrado
        if not input:
            raise InputCSRFError('Input CSRF não encontrado no corpo html')

        # pega o valor do input, no caso um CSRF Token valido
        csrf = self.soup.find("input", {"name": "csrf"})['value']
        return csrf
