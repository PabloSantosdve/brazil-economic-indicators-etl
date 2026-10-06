import requests

def extrair_serie_bcb(serie_id, data_inicial, data_final):
    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie_id}/dados"
        f"?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
    )
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    ipca = extrair_serie_bcb(433, "01/10/2021", "05/10/2026")
    selic = extrair_serie_bcb(432, "01/10/2021", "05/10/2026")
    dolar = extrair_serie_bcb(1, "01/10/2021", "05/10/2026")
    print(len(ipca))
    print(len(selic))
    print(len(dolar))
