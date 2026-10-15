"""Etapa Transform do pipeline ETL de indicadores econômicos do Brasil.

Este arquivo recebe as três séries do Banco Central (dólar, Selic e IPCA) já
buscadas pela etapa Extract, limpa cada uma, resume tudo em base mensal e junta
numa tabela única. Quem chama as etapas em ordem é o main.py.

Séries usadas (API SGS do Banco Central):
    - 1   -> Dólar (USD/BRL), uma cotação por dia útil
    - 432 -> Meta da Selic definida pelo Copom, em % ao ano, um valor por dia
    - 433 -> IPCA, variação mensal em % no mês, um valor por mês (dia 1)
"""

import pandas as pd


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


def montar_tabela_mensal(ipca: list, selic: list, dolar: list) -> pd.DataFrame:
    """Monta a tabela mensal única a partir das três séries cruas.

    Etapas:
        1. transforma cada lista em uma tabela e limpa os tipos;
        2. resume cada série para uma linha por mês;
        3. renomeia as colunas e junta as três lado a lado;
        4. descarta os meses em que alguma das três séries ainda não tem dado.

    Args:
        ipca: lista de dicionários devolvida pela API para a série 433.
        selic: lista de dicionários devolvida pela API para a série 432.
        dolar: lista de dicionários devolvida pela API para a série 1.
            Cada item tem o formato {'data': '05/10/2026', 'valor': '5.2204'}.

    Returns:
        DataFrame com o mês (dia 1) no índice, chamado 'data', e as colunas
        'ipca', 'selic' e 'dolar'. A tabela termina no último mês em que as
        três séries estão disponíveis.
    """
    # Transforma cada lista de dicionários em uma tabela (DataFrame) do pandas.
    ipca_df = pd.DataFrame(ipca)
    selic_df = pd.DataFrame(selic)
    dolar_df = pd.DataFrame(dolar)

    # Limpa os tipos de cada série (data vira data, valor vira número).
    ipca_transformed = transform_data(ipca_df)
    selic_transformed = transform_data(selic_df)
    dolar_transformed = transform_data(dolar_df)

    # Resume cada série para uma linha por mês.
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
    # diferentes antes de serem juntadas. Os nomes em minúsculas precisam
    # combinar com as chaves do dicionário FORMATOS no load.py. O inplace=True
    # altera a própria tabela em vez de criar uma cópia.
    dolar_mensal.rename(columns={'valor': 'dolar'}, inplace=True)
    selic_mensal.rename(columns={'valor': 'selic'}, inplace=True)
    ipca_mensal.rename(columns={'valor': 'ipca'}, inplace=True)

    # Junta as três tabelas em uma só.
    # pd.concat com axis=1 coloca as tabelas lado a lado (as colunas se somam),
    # alinhando as linhas pelo índice, que é o mês. O dropna() em seguida
    # descarta os meses em que alguma coluna está vazia. Isso acontece nos
    # meses mais recentes, em que o IPCA ainda não foi divulgado, e também no
    # mês parcial em andamento.
    df_mensal = pd.concat([ipca_mensal, selic_mensal, dolar_mensal], axis=1).dropna()

    return df_mensal