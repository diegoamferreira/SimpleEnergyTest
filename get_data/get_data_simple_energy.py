import asyncio
import json
import time
from typing import Any

import httpx
import pandas as pd
from decouple import config

from errors.simple_energy_errors import ClientCodeNotFound
from extract_file.extract_barcode_file import ExtractBarcodeFile
from parse_data.parse_csrf_token import ParseCSRFToken
from parse_data.parse_files_list import ParseFilesList

# Acessando variaveis de ambiente

# Url base alvo
BASE_URL = config('BASE_URL', default='https://simpleenergy.com.br/teste/')
# Tempo de espera entre cada requisição
REQ_INTERVAL_SECONDS = config('REQ_INTERVAL_SECONDS', default=0, cast=int)
# Define a quantidade maxima de requisições em "paralelo"
MAX_CONCURRENCY = config('MAX_CONCURRENCY', default=5, cast=int)


class GetDataSimpleEnergy:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
         Chrome/110.0.0.0 Safari/537.36"
    }

    def __init__(self, client_codes: list, active_proxie: bool = False, base_url: str = BASE_URL,
                 max_concurrency: int = MAX_CONCURRENCY) -> None:
        self.client_codes = client_codes
        self.active_proxie = active_proxie
        self.max_concurrency = max_concurrency
        self.base_url = base_url
        self.intervalo_de_requisicao = REQ_INTERVAL_SECONDS
        self.boletos = []

    def get_all_boletos(self, output_format: str = 'dict') -> Any:
        """
        Coleta os boletos de forma assíncrona e responde no formato solicitado.
        :param client_codes: Lista de coóigos dos clientes para requisição dos boletos
        :param output_format: Formato de saída escolhido
        :return: Boletos no formato desejado
        """
        boletos = asyncio.run(self.__orchestrator())

        if not boletos:
            return

        self.boletos = boletos

        return self.__format_output(output_format)

    def __format_output(self, output_format: str) -> Any:
        """Processa os diferentes tipos de respostas disponíveis"""
        if output_format == 'dict':
            return self.boletos
        elif output_format == 'df':
            return pd.DataFrame(self.boletos)
        elif output_format == 'json_file':
            filename = f"output/{''.join(self.client_codes)}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.boletos, f, indent=4, ensure_ascii=False)
            return f'arquivo: {filename} salvo'
        elif output_format == 'csv_file':
            filename = f"output/{''.join(self.client_codes)}.csv"
            pd.DataFrame(self.boletos).to_csv(filename)
            return f'arquivo: {filename} salvo'
        else:
            return f'FORMATO INVÁLIDO: {output_format}'

    async def __orchestrator(self) -> list:
        """
        Coleta todos os boletos passados como parametro de forma assíncrona.
        :return: Boletos raspados da plataforma.
        """

        tasks = []
        async with httpx.AsyncClient(headers=self.headers, **self.__get_proxies()) as session:
            for cli_code in self.client_codes:
                tasks.append(
                    self.__get_data_safe(cli_code, session)
                )

            # Executando a tasks de forma assincrona
            boletos = await asyncio.gather(*tasks)

        # Convertendo lista de listas em uma lista única
        boletos_flat = [x for xs in boletos for x in xs]

        return boletos_flat

    async def __execute_extract_boleto(self, client_code: str, session: httpx.AsyncClient) -> list:
        """
        Pipeline de dados para extração de boletos de forma assíncrona
        :param client_code: Código do boleto
        :param session: Sessão da requisição
        :return: Dicionário com os codigos de barras extraídos dos boletos
        """
        # Garante um CSRF válido para envio de POST
        csrf = await self.__get_csrf_token(session=session)

        # Pega a lista com todos os arquivos disponíveis na página
        try:
            boletos_in_page = await self.__get_boletos_from_page(csrf=csrf, client_code=client_code, session=session)
        except ClientCodeNotFound:
            return []

        # Abre todos os arquivos e coleta os dados deles
        boletos_prontos = await self.__get_boleto_barcode(boletos_in_page=boletos_in_page, session=session)

        return boletos_prontos

    async def __get_csrf_token(self, session: httpx.AsyncClient) -> str:
        """
        Precisamos do csrf para garantir uma requisição post valida.
        :return: CSRF
        """
        response = await session.get(self.base_url)

        csrf = ParseCSRFToken(response=response).parse()

        return csrf

    async def __get_boletos_from_page(self, csrf: str, client_code: str, session: httpx.AsyncClient) -> list:
        """
        Requisição post usando codigo e csrf para coletar lista com boletos disponíveis na página
        :param client_code: Código do cliente
        :return: Lista de boletos disponíveis na página
        """
        form_data = {
            'codigo': client_code,
            'csrf': csrf
        }
        self.__aguardar_intervalo_de_requisicao()
        response = await session.post(self.base_url, data=form_data)

        if response.status_code == 404:
            raise ClientCodeNotFound(f'Codigo do cliente não encontrado. Cod: {client_code}')
        file_list = ParseFilesList(response=response).parse()

        return file_list

    async def __get_boleto_barcode(self, boletos_in_page: list, session: httpx.AsyncClient) -> list:
        """
        Adiciona o codigo de barras em cada boleto
        :return: Dicionário com todos os boletos e seus respecitivos codigos de barra.
        """
        for boleto in boletos_in_page:
            self.__aguardar_intervalo_de_requisicao()
            response = await session.get(f"{self.base_url}/{boleto['href']}")
            barcode = ExtractBarcodeFile(response=response).execute()
            boleto['barcode'] = barcode
        return boletos_in_page

    def __aguardar_intervalo_de_requisicao(self) -> None:
        """Quando executado aguarda o tempo definido no atributo intervalo_de_requisicao"""
        if self.intervalo_de_requisicao:
            time.sleep(self.intervalo_de_requisicao)

    def __get_proxies(self) -> dict:
        """
        Define o proxie utilizado nas chamadas
        """
        if self.active_proxie:
            # FAKE PROXIE
            return {
                'proxies': 'http://0.0.0.0:8888',
            }
        return {}

    async def __get_data_safe(self, client_code: str, session: httpx.AsyncClient) -> list:
        # Limitando a quantidade de requisições assíncronas
        limit = asyncio.Semaphore(self.max_concurrency)
        async with limit:
            return await self.__execute_extract_boleto(client_code=client_code, session=session)
