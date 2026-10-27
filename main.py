from datetime import date

from extract import extrair_serie_bcb
from transform import montar_tabela_mensal
from load import salvar_excel, salvar_csv
from grafico_ipca import plotar_ipca
from grafico_dolar_selic import plotar_dolar_selic

ANOS_DE_HISTORICO = 5

SERIE_IPCA = 433
SERIE_SELIC = 432
SERIE_DOLAR = 1

# Onde salvar as imagens dos gráficos.
IMAGEM_IPCA = "grafico_ipca.png"
IMAGEM_DOLAR_SELIC = "grafico_dolar_selic.png"


def main():
    """Roda o pipeline completo: Extract, Transform e Load."""
    # --- DATAS ---
    # A data final é hoje. A data inicial é o dia 1 do mesmo mês, ANOS_DE_HISTORICO
    # anos atrás. O dia 1 garante que o IPCA do primeiro mês (sempre datado no dia
    # 1) entre no resultado. O replace com ano e dia juntos também evita erro se
    # o programa rodar em 29 de fevereiro.
    hoje = date.today()
    data_inicial = hoje.replace(year=hoje.year - ANOS_DE_HISTORICO, day=1)
    data_final = hoje

    # A API espera as datas como texto no formato dd/mm/aaaa.
    inicio = data_inicial.strftime('%d/%m/%Y')
    fim = data_final.strftime('%d/%m/%Y')
    print(f"Período: {inicio} a {fim}")

    # EXTRACT: busca as três séries na API do Banco Central 
    ipca = extrair_serie_bcb(SERIE_IPCA, inicio, fim)
    selic = extrair_serie_bcb(SERIE_SELIC, inicio, fim)
    dolar = extrair_serie_bcb(SERIE_DOLAR, inicio, fim)

    # TRANSFORM: limpa, resume por mês e junta numa tabela única 
    df_mensal = montar_tabela_mensal(ipca, selic, dolar)

    # LOAD: salva a tabela final em Excel e em CSV 
    salvar_excel(df_mensal, "data/indicadores_mensais.xlsx")
    salvar_csv(df_mensal, "data/indicadores_mensais.csv")

    # GRÁFICOS: desenha os gráficos de exemplo e salva as imagens 
    # Usamos a tabela que já está na memória, sem ler o CSV de novo. As funções
    # só salvam o PNG (não abrem janela), então o pipeline não trava.
    plotar_ipca(df_mensal, IMAGEM_IPCA)
    plotar_dolar_selic(df_mensal, IMAGEM_DOLAR_SELIC)

    # Resumo no terminal, para conferir o resultado.
    print(df_mensal.tail())
    print(f"{len(df_mensal)} meses salvos em data/")
    print(f"Gráficos salvos: {IMAGEM_IPCA} e {IMAGEM_DOLAR_SELIC}")


# Este bloco só roda quando o arquivo é executado diretamente (python main.py).
# Se outro arquivo fizer "import main", o pipeline não dispara sozinho.
if __name__ == "__main__":
    main()