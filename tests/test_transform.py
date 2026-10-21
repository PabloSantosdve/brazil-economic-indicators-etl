import pandas as pd
import pytest
from transform import transform_data


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