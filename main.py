import argparse

from src.get_data.get_data_simple_energy import GetDataSimpleEnergy

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--codigo', nargs='+', required=True, help='Código dos clientes (1+)')
parser.add_argument('-f', '--format', choices=['dict', 'df', 'json_file', 'csv_file'], default='dict')
args = parser.parse_args()


def main(client_code_list: list, output_format: str = 'dict'):
    get_boleto = GetDataSimpleEnergy(client_code_list)
    boletos = get_boleto.get_all_boletos(output_format)
    return boletos


if __name__ == '__main__':
    client_code_list = args.codigo
    output_format = args.format
    response = main(client_code_list=client_code_list, output_format=output_format)
    print(response)

    # Coletando somente 1 codigo
    # response_1 = main(client_code='321465')
    # print(response_1)
    #
    # Coletando mais de 1 codigo de forma assíncrona
    # response_2 = main(client_code=['321465', '98465'])
    # print(response_2)

    # # Coletando mais de 1 codigo tendo a saída como DataFrame (pandas)
    # response_3 = main(client_code=['321465', '98465'], output_format='df')
    # print(response_3)
    #
    # # Coletando mais de 1 codigo tendo a saída como um arquivo json
    # response_4 = main(client_code=['321465', '98465'], output_format='json_file')
    # print(response_4)
    #
    # # Coletando mais de 1 codigo tendo a saída como um arquivo json
    # response_5 = main(client_code=['321465', '98465'], output_format='csv_file')
    # print(response_5)
