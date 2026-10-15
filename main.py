from datetime import date
from extract import extrair_serie_bcb as baixar_serie
from transform import montar_tabela_mensal
from load import salvar_excel, salvar_csv

SERIE_IPCA = 433
SERIE_SELIC = 432
SERIE_DOLAR = 1

def main():
    hoje = date.today()
    data_inicial = hoje.replace(year=hoje.year - 5, day=1)
    data_final = hoje

    # API espera as datas como texto no formato dia/mês/ano. O strftime faz essa conversão.
    inicio = data_inicial.strftime("%d/%m/%Y")
    fim = data_final.strftime("%d/%m/%Y")
    print(f"Baixando dados de {inicio} a {fim}...")

    #Extract 
    ipca = baixar_serie(SERIE_IPCA, inicio, fim)
    selic = baixar_serie(SERIE_SELIC, inicio, fim)
    dolar = baixar_serie(SERIE_DOLAR, inicio, fim)

    #Transform
    df_mensal = montar_tabela_mensal(ipca, selic, dolar)

    #Load
    salvar_excel(df_mensal, "data/indicadores_mensais.xlsx")
    salvar_csv(df_mensal, "data/indicadores_mensais.csv")

    #Resumo no terminal 
    print(df_mensal.tail())
    print(f"{len(df_mensal)} meses salvos em data/indicadores_mensais.xlsx e .csv")

#Este bloco só roda se o arquivo for executado diretamento (python main.py)
#Se outro arquivo fizer "import main", o pipeline não dispara sozinho
if __name__ == "__main__":
    main()