import httpx
from bs4 import BeautifulSoup

from errors.simple_energy_errors import ResposeStatusCodeError


class ParseResponseSoup:

    def __init__(self, response: httpx.Response):
        if response.status_code != 200:
            raise ResposeStatusCodeError('Status Code inválido ao pegar o CSRF Token', status_code=response.status_code)
        self.soup = BeautifulSoup(response.content, 'html.parser')
