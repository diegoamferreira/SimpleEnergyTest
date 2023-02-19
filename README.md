# Teste Simple Energy

---

### Objetivo

> Raspar "código de barras" de maneira dinâmica de arquivos encontrados em página web, conteúdo varia de acordo com o "
> código do cliente" (código fornecido)

---

Informações importantes

* Os codigos fornecidos estão sendo considerados como CODIGO DO CLIENTE.
* Consulta assíncrona para tratar grandes quantidades se necessário
    * **controle de concorrencia**: evitar problemas com o site alvo
    * **Proxies**: pronto para adição de proxies ao codigo para evitar bloqueios pelo IP

---

### Versão Python

* [Python 3.11.2](https://www.python.org/)

### Como rodar esse projeto?

1. Clone esse repositório.
2. Crie um ambiente virtual com python3.
3. Ative o virtualenv.
4. Instale as dependências.

---

### Iniciando o projeto

```
git clone https://github.com/diegoamferreira/SympleEnergyTest.git
cd SympleEnergyTest
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Rodando testes

```
pytest -v
```

### Rodando o programa

#### Parametros aceitos

##### codigo

* `-c`**codigo** (--codigo) _obrigatorio_
    * 1 ou mais códigos de clientes para raspagem dos códigos de barras
        * exemplo 1: `python main.py -c 321465 98465`
        * exemplo 2: `python main.py -c 321465 98465 131313`
        * exemplo 3: `python main.py -c 321465`

---

* `-f`**format** (--format) _opcional_
    * formato de saída dos dados, opções:
        * `dict` - (default) _Dicionário python impresso no console_
        * `df` - _DataFrame Pandas impresso no console_
        * `json_file` - _Arquivo JSON salvo na pasta raiz do programa, nome do arquivo vai ser impresso no console_
        * `csv_file` - _Arquivo CSV salvo na pasta raiz do programa, nome do arquivo vai ser impresso no console_
            * exemplo 1: `python main.py -c 321465 98465 -f dict`
            * exemplo 2: `python main.py -c 321465 98465 -f df`
            * exemplo 3: `python main.py -c 321465 98465 -f json_file`
            * exemplo 4: `python main.py -c 321465 98465 -f csv_file`

---

### EXEMPLO DE EXECUÇÃO

##### Executando com os códigos de clientes: `321465` e `98465` e com a saída em json salva na raiz do projeto.

`python main.py -c 321465 98465 -f json_file`

---

### Variaveis de ambiente

* `BASE_URL`
  * > _(default: 'https://simpleenergy.com.br/teste/')_ Url base alvo das requisições, se algo mudar na url do site alvo, alterar essa variavel de ambiente.
* `REQ_INTERVAL_SECONDS`
  * > _(default: '0')_ Tempo de espera entre cada requisição: Se precisar forçar um tempo de espera entre cada passo executado da raspagem,
   defina aqui em SEGUNDOS.
* `MAX_CONCURRENCY`
  * > _(default: '5')_ Define a quantidade maxima de requisições em "paralelo" no site alvo.

---

### Etapas do projeto (FAKE)

- [x] Aplicação funcional offline
- [ ] Deploy em lambda AWS
- [ ] Api serverless