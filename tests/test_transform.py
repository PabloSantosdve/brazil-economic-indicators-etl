import pandas as pd
import pytest
from transform import transform_data, montar_tabela_mensal


def test_transform_data_converte_ordena_e_descarta_invalidos():
    # 1. montar a tabela de entrada (datas fora de ordem e um valor inválido)
    df_input = pd.DataFrame({
        'data': ['15/02/2020', '01/01/2020', '15/03/2020'],
        'valor': ['2.5', '1.5', 'abc']
    })
    # 2. chamar a transform_data e guardar o resultado
    df_output = transform_data(df_input)
    # 3. conferir com assert
    assert len(df_output) == 2  # só duas linhas válidas
    assert df_output['valor'].iloc[0] == 1.5  # a primeira linha é a data mais antiga


def test_transform_data_data_invalida_levanta_erro():
    # 1. montar a tabela com uma data que não existe (30 de fevereiro)
    df_input = pd.DataFrame({
        'data': ['30/02/2020'],
        'valor': ['1.5']
    })
    # 2. chamar a transform_data e esperar que levante um erro
    with pytest.raises(ValueError):
        transform_data(df_input)

def test_montar_tabela_mensal_resume_e_junta_as_series():
    # 1. dados de entrada, no formato que a API devolve (tudo em texto)
    ipca = [
        {'data': '01/01/2020', 'valor': '0.21'},
        {'data': '01/02/2020', 'valor': '0.25'},
    ]
    selic = [
        {'data': '02/01/2020', 'valor': '4.50'},
        {'data': '20/01/2020', 'valor': '4.25'},
        {'data': '05/02/2020', 'valor': '4.00'},
    ]
    dolar = [
        {'data': '02/01/2020', 'valor': '4.0'},
        {'data': '20/01/2020', 'valor': '6.0'},
        {'data': '05/02/2020', 'valor': '5.0'},
    ]

    # 2. chamar a função, na ordem (ipca, selic, dolar)
    df = montar_tabela_mensal(ipca, selic, dolar)

    # 3. conferir o resultado
    assert len(df) == 2                                # janeiro e fevereiro
    assert list(df.columns) == ['ipca', 'selic', 'dolar']
    assert df['dolar'].iloc[0] == 5.0                  # média de 4.0 e 6.0
    assert df['selic'].iloc[0] == 4.25                 # último valor de janeiro
    assert df['ipca'].iloc[0] == 0.21                  # IPCA de janeiro
    assert df['dolar'].iloc[1] == 5.0                  # fevereiro (um só valor)
    assert df['selic'].iloc[1] == 4.00                 # fevereiro (um só valor)
    