"""Etapa Extract do pipeline ETL de indicadores econômicos do Brasil.

Este arquivo busca séries temporais na API de dados abertos do Banco Central
do Brasil (SGS - Sistema Gerenciador de Séries Temporais).

Séries usadas no projeto:
    - 1   -> Dólar (USD/BRL), uma cotação por dia útil
    - 432 -> Meta da Selic definida pelo Copom, em % ao ano, um valor por dia
    - 433 -> IPCA, variação mensal em % no mês, um valor por mês (dia 1)
"""

import requests


def extrair_serie_bcb(serie_id, data_inicial, data_final):
    """Busca uma série do Banco Central para um período e devolve os dados.

    Args:
        serie_id: código numérico da série no SGS (por exemplo, 1 para o dólar).
        data_inicial: primeira data do período, no formato "dd/mm/aaaa".
        data_final: última data do período, no formato "dd/mm/aaaa".

    Returns:
        Uma lista de dicionários, um por registro, no formato
        {'data': '05/10/2026', 'valor': '5.2204'}. Atenção: tanto a data quanto
        o valor chegam como texto. A conversão para data e número é feita na
        etapa Transform.

    Raises:
        requests.HTTPError: se a API responder com um status de erro (por
            exemplo, série inexistente ou período acima do limite).
        requests.Timeout: se a API não responder em 30 segundos.

    Observação:
        Segundo a documentação do Banco Central, consultas por período são
        limitadas a 10 anos.
    """
    # Monta o endereço da consulta. As duas f-strings entre parênteses são
    # coladas pelo Python em um único texto. O "?" separa o caminho dos
    # parâmetros, e o "&" separa um parâmetro do outro. Aqui, os parâmetros
    # pedem o formato JSON e o intervalo de datas.
    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie_id}/dados"
        f"?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
    )

    # Faz o pedido à API. O timeout=30 limita a espera a 30 segundos: sem ele,
    # o programa poderia ficar travado para sempre se a API não respondesse.
    response = requests.get(url, timeout=30)

    # Se o status da resposta indicar erro (qualquer coisa diferente de sucesso,
    # como 404 ou 500), levanta uma exceção na hora. Assim o pipeline falha de
    # forma clara no ponto certo, em vez de seguir adiante com dados vazios.
    response.raise_for_status()

    # Converte o JSON recebido em uma lista de dicionários do Python.
    return response.json()


# Este bloco só roda quando o arquivo é executado diretamente
# (python extract.py). Quando outro arquivo faz "from extract import ...", o
# bloco é ignorado, e só a função fica disponível para uso.
if __name__ == "__main__":
    # Período de 5 anos. A data inicial no dia 1 garante que o IPCA de
    # outubro de 2021 (cuja data é 01/10/2021) entre no resultado.
    ipca = extrair_serie_bcb(433, "01/10/2021", "05/10/2026")
    selic = extrair_serie_bcb(432, "01/10/2021", "05/10/2026")
    dolar = extrair_serie_bcb(1, "01/10/2021", "05/10/2026")

    # Confere a quantidade de registros de cada série (len conta os itens da
    # lista). Resultados esperados, aproximadamente: IPCA 59, Selic 1831 e
    # dólar 1258.
    print(len(ipca))
    print(len(selic))
    print(len(dolar))