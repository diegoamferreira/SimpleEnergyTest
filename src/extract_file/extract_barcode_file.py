import io

import httpx
from pypdf import PdfReader

from errors.simple_energy_errors import FormatFileError, ResposeStatusCodeError


class ExtractBarcodeFile:

    def __init__(self, response: httpx.Response) -> None:
        """
        :param response: Resposta da requisição com status 200
        """
        if response.status_code != 200:
            raise ResposeStatusCodeError('Status Code != 200', status_code=response.status_code)

        self.content = response.content
        self.filetype = str(response.url).split('.')[-1]

    def execute(self) -> str:
        """
        Executa a extração do código de barra com base no tipo de arquivo
        :return: Código de barras
        """
        if self.filetype == 'pdf':
            return self.__extract_pdf_barcode()
        elif self.filetype == 'txt':
            return self.__extract_txt_barcode()
        else:
            raise FormatFileError('Tipo de arquivo não esperado', file_format=self.filetype)

    def __extract_pdf_barcode(self) -> str:
        """
        Usa PyPDF2 para ler o pdf como BytesIO e ler seu conteúdo.
        :return: Código de barras
        """
        # Executa as tratativas necessárias...
        with io.BytesIO(self.content) as data:
            reader = PdfReader(data)
            page = reader.pages[0]
            return page.extract_text()

    def __extract_txt_barcode(self) -> str:
        """
        Faz o decode da resposta http para pegar o código de barras.
        :return: Código de barras
        """
        # Executa as tratativas necessárias...
        return self.content.decode()
