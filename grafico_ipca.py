"""Gera o gráfico do IPCA mês a mês a partir do CSV criado pelo main.py.

Para rodar (depois de rodar python main.py pelo menos uma vez):

    python grafico_ipca.py
"""

import matplotlib.pyplot as plt
import pandas as pd

CAMINHO_CSV = "data/indicadores_mensais.csv"
CAMINHO_IMAGEM = "grafico_ipca.png"


def plotar_ipca(tabela_mensal: pd.DataFrame, caminho_imagem: str) -> None:
    """Desenha o IPCA de cada mês em barras e salva a imagem em PNG.

    Args:
        tabela_mensal: tabela com o mês (dia 1) no índice e a coluna 'ipca'.
        caminho_imagem: onde salvar o PNG, por exemplo "grafico_ipca.png".
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    # Uma barra por mês. O width é em dias: 25 deixa as barras largas, com um
    # pequeno espaço entre uma e outra.
    barras = ax.bar(tabela_mensal.index, tabela_mensal['ipca'], width=25, color='#1F4E78')

    # Escreve o valor de cada mês em cima da barra, na vertical para caber.
    ax.bar_label(barras, fmt='%.2f', rotation=90, fontsize=7, padding=3)

    ax.set_title('IPCA mês a mês (inflação, % no mês)')
    ax.set_ylabel('% no mês')
    ax.grid(axis='y', alpha=0.3)
    ax.axhline(0, color='black', linewidth=0.8)
    fig.autofmt_xdate()
    fig.tight_layout()
    ax.margins(y=0.1)

    fig.savefig(caminho_imagem, dpi=150)
    plt.show()


if __name__ == "__main__":
    df = pd.read_csv(CAMINHO_CSV, index_col='data', parse_dates=True)
    plotar_ipca(df, CAMINHO_IMAGEM)