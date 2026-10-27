import matplotlib.pyplot as plt
import pandas as pd

CAMINHO_CSV = "data/indicadores_mensais.csv"
CAMINHO_IMAGEM = "grafico_dolar_selic.png"


def rotular_pontos(ax, serie: pd.Series, formato: str, cor: str) -> None:
    """Escreve o valor nos pontos que mais importam: primeiro, último, máximo e mínimo.

    Rotular os 59 meses deixaria o gráfico ilegível, então só marcamos os
    pontos que contam a história da série.

    Args:
        ax: o gráfico onde escrever.
        serie: a série (índice = mês, valores = números).
        formato: modelo do texto, por exemplo "R$ {:.2f}".
        cor: cor da bolinha e do texto.
    """
    # Um conjunto não repete datas: se um ponto cumprir dois papéis (por exemplo,
    # o último ser também o máximo), o rótulo aparece uma vez só.
    datas = {serie.index[0], serie.index[-1], serie.idxmax(), serie.idxmin()}
    for data in datas:
        valor = serie[data]
        ax.plot(data, valor, 'o', color=cor)

        # Posição do texto em relação à bolinha (em pontos):
        #   primeiro ponto -> à esquerda; último -> à direita;
        #   mínimo -> embaixo; máximo -> em cima.
        # Primeiro e último ficam nas pontas para não colidir com o máximo.
        if data == serie.index[-1]:
            deslocamento, alinhamento = (8, -3), 'left'
        elif data == serie.index[0]:
            deslocamento, alinhamento = (-8, -3), 'right'
        elif data == serie.idxmin():
            deslocamento, alinhamento = (0, -16), 'center'
        else:
            deslocamento, alinhamento = (0, 8), 'center'

        ax.annotate(formato.format(valor), xy=(data, valor),
                    xytext=deslocamento, textcoords='offset points',
                    ha=alinhamento, fontsize=9, fontweight='bold', color=cor)


def plotar_dolar_selic(tabela_mensal: pd.DataFrame, caminho_imagem: str) -> None:
    """Desenha o dólar (em cima) e a Selic (embaixo) e salva a imagem em PNG.

    Args:
        tabela_mensal: tabela com o mês (dia 1) no índice e as colunas
            'dolar' e 'selic'.
        caminho_imagem: onde salvar o PNG, por exemplo "grafico_dolar_selic.png".
    """
    # Cria a figura com dois gráficos, um em cima do outro (2 linhas, 1 coluna).
    # O sharex=True faz os dois usarem os mesmos meses na horizontal, alinhados.
    fig, (ax_dolar, ax_selic) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    # Gráfico de cima: dólar (média mensal), em reais.
    ax_dolar.plot(tabela_mensal.index, tabela_mensal['dolar'],
                  color='#1F4E78', linewidth=2)
    rotular_pontos(ax_dolar, tabela_mensal['dolar'], 'R$ {:.2f}', '#1F4E78')
    ax_dolar.margins(x=0.08, y=0.2)
    ax_dolar.set_title('Dólar (média mensal)')
    ax_dolar.set_ylabel('R$')
    ax_dolar.grid(alpha=0.3)

    # Gráfico de baixo: Selic (valor no fim do mês), em % ao ano.
    # O drawstyle='steps-post' desenha a Selic em "degraus", porque ela só muda
    # nas reuniões do Copom e fica constante entre uma reunião e outra.
    ax_selic.plot(tabela_mensal.index, tabela_mensal['selic'],
                  color='#C55A11', linewidth=2, drawstyle='steps-post')
    rotular_pontos(ax_selic, tabela_mensal['selic'], '{:.2f}%', '#C55A11')
    ax_selic.margins(x=0.08, y=0.2)
    ax_selic.set_title('Selic (meta, fim do mês)')
    ax_selic.set_ylabel('% ao ano')
    ax_selic.grid(alpha=0.3)

    fig.suptitle('Dólar e Selic mês a mês', fontsize=14, fontweight='bold')
    fig.autofmt_xdate()
    fig.tight_layout()

    fig.savefig(caminho_imagem, dpi=150)
    plt.show()


if __name__ == "__main__":
    df = pd.read_csv(CAMINHO_CSV, index_col='data', parse_dates=True)
    plotar_dolar_selic(df, CAMINHO_IMAGEM)