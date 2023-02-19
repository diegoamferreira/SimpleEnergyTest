from src.parse_data.parse_response import ParseResponseSoup


class ParseFilesList(ParseResponseSoup):

    def parse(self) -> list:
        """
        Organiza as informações dos boletos
        :return: lista com os boletos encontrados na página
        """
        # Buscando o código
        title_page = self.soup.title
        if not title_page:
            return []
        client_code = int(self.soup.title.text.split()[-1])

        # Buscando as informações dos boletos
        boletos = []
        for div in self.soup.find_all('div')[1:]:
            arquivo_div = div.find('div')
            if arquivo_div:
                arquivo = arquivo_div.text
                links = div.find_all('a')
                for link in links:
                    href = link['href']
                    nome = link.text
                    boletos.append({'client_code': client_code, 'arquivo': arquivo, 'href': href, 'nome': nome})

        # Se nenhum boleto for encontrado, devolver um dicionário vazio
        if not boletos:
            return []

        return boletos
