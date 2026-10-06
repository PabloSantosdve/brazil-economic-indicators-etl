"""Etapa Transform do pipeline ETL de indicadores econômicos do Brasil.

Este arquivo pega as três séries do Banco Central (dólar, Selic e IPCA),
limpa cada uma, resume tudo em base mensal e junta numa tabela única.

Séries usadas (API SGS do Banco Central):
    - 1   -> Dólar (USD/BRL), uma cotação por dia útil
    - 432 -> Meta da Selic definida pelo Copom, em % ao ano, um valor por dia
    - 433 -> IPCA, variação mensal em % no mês, um valor por mês (dia 1)
"""

import pandas as pd
from extract import  extrair_serie_bcb


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpa uma série do Banco Central que já está em um DataFrame.

    A API devolve tudo como texto, então esta função:
        1. converte a coluna 'data' de texto (dd/mm/aaaa) para data de verdade;
        2. converte a coluna 'valor' de texto para número;
        3. remove as linhas cujo valor não pôde ser convertido;
        4. ordena da data mais antiga para a mais recente e refaz o índice.

    Args:
        df: DataFrame com as colunas 'data' e 'valor', ambas em texto,
            exatamente como vêm da API.

    Returns:
        DataFrame com 'data' no tipo datetime64 e 'valor' no tipo float64.

    Observação:
        Os passos 1 e 2 alteram o DataFrame original recebido. Os passos 3 e 4
        criam novas tabelas, então só o DataFrame retornado está completamente
        limpo.
    """
    # Converte as datas de texto ("05/10/2026") para data de verdade.
    # O parâmetro format avisa que o formato é dia/mês/ano. Sem ele, o pandas
    # poderia confundir com mês/dia. Se alguma data vier inválida, o código
    # para com erro (de propósito, para o problema não passar despercebido).
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')

    # Converte os valores de texto ("5.2204") para número, permitindo contas.
    # errors='coerce' transforma qualquer valor inválido em NaN (vazio) em vez
    # de dar erro.
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')

    # Remove as linhas em que 'valor' ficou vazio. O subset limita a checagem
    # a essa coluna.
    df = df.dropna(subset=['valor'])

    # Ordena da data mais antiga para a mais recente. O reset_index refaz a
    # numeração das linhas (0, 1, 2...) e drop=True descarta a numeração antiga
    # em vez de guardá-la como coluna.
    df = df.sort_values(by='data').reset_index(drop=True)
    return df


if __name__ == "__main__":
    # --- EXTRACT: busca as três séries na API do Banco Central ---
    # Período de 5 anos. A data inicial no dia 1 garante que o IPCA de
    # outubro de 2021 (cuja data é 01/10/2021) entre no resultado.
    ipca = extrair_serie_bcb(433, "01/10/2021", "05/10/2026")
    selic = extrair_serie_bcb(432, "01/10/2021", "05/10/2026")
    dolar = extrair_serie_bcb(1, "01/10/2021", "05/10/2026")

    # Transforma cada lista de dicionários devolvida pela API em uma tabela
    # (DataFrame) do pandas.
    ipca_df = pd.DataFrame(ipca)
    selic_df = pd.DataFrame(selic)
    dolar_df = pd.DataFrame(dolar)

    # --- TRANSFORM, parte 1: limpa os tipos de cada série ---
    ipca_transformed = transform_data(ipca_df)
    selic_transformed = transform_data(selic_df)
    dolar_transformed = transform_data(dolar_df)

    # --- TRANSFORM, parte 2: resume cada série para uma linha por mês ---
    # resample('MS', on='data') agrupa as linhas por mês, usando a coluna
    # 'data'. O 'MS' (month start) marca cada mês com o primeiro dia dele.
    # O que vem depois do resample escolhe como resumir cada mês:
    #   .last() -> valor mais recente do mês. Usado no IPCA (que já tem um valor
    #              por mês) e na Selic (a meta é um "degrau", e o último valor
    #              mostra a taxa em vigor no fim do mês).
    #   .mean() -> média do mês. Usada no dólar, para suavizar as oscilações
    #              do dia a dia.
    ipca_mensal = ipca_transformed.resample('MS', on='data').last()
    selic_mensal = selic_transformed.resample('MS', on='data').last()
    dolar_mensal = dolar_transformed.resample('MS', on='data').mean()

    # Renomeia a coluna 'valor' de cada tabela, para que as três tenham nomes
    # diferentes antes de serem juntadas. O inplace=True altera a própria tabela
    # em vez de criar uma cópia.
    dolar_mensal.rename(columns={'valor': 'dolar'}, inplace=True)
    selic_mensal.rename(columns={'valor': 'selic'}, inplace=True)
    ipca_mensal.rename(columns={'valor': 'ipca'}, inplace=True)

    # --- TRANSFORM, parte 3: junta as três tabelas em uma só ---
    # pd.concat com axis=1 coloca as tabelas lado a lado (as colunas se somam),
    # alinhando as linhas pelo índice, que é o mês. O dropna() em seguida
    # descarta os meses em que alguma coluna está vazia. Hoje isso acontece nos
    # meses mais recentes, em que o IPCA ainda não foi divulgado, e também no
    # mês parcial em andamento. A tabela termina, portanto, no último mês em
    # que as três séries estão disponíveis.
    df_mensal = pd.concat([ipca_mensal, selic_mensal, dolar_mensal], axis=1).dropna()

    # Confere o resultado: as 5 primeiras linhas, as 5 últimas e o total de meses.
    print(df_mensal.head())
    print(df_mensal.tail())
    print(len(df_mensal))