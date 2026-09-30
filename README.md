# brazil-economic-indicators-etl

🇬🇧 English | [🇧🇷 Português](#-português)

> 🚧 **Status: in development.** The project is being built step by step. This README will be updated as each stage is completed.

## 🇬🇧 English

### Overview

A simple, beginner-friendly **ETL (Extract, Transform, Load) pipeline** in Python. It collects three key Brazilian economic indicators from the Brazilian Central Bank (BCB) open data API and combines them into a **single, analysis-ready dataset**.

| Indicator | Description |
|---|---|
| **USD/BRL** | US dollar exchange rate in Brazilian reais (daily) |
| **Selic** | Brazilian benchmark interest rate |
| **IPCA** | Brazilian consumer price inflation (monthly) |

The default time window is the **last 5 years**.

### Why this project?

Economic series are published at different frequencies (daily, monthly) and in raw text formats. This pipeline handles the boring part — fetching, cleaning and aligning the data — so you can focus on analysis.

### How it works

```
Extract  →  Transform  →  Load
  BCB API     clean, convert,   single table
  (3 series)  align frequencies (SQLite)
```

1. **Extract:** fetch the three series from the BCB SGS open data API.
2. **Transform:** convert text to numbers and dates, and align series with different frequencies into one table.
3. **Load:** store the final dataset so anyone can query it.

### Example analyses (planned)

- Month-by-month inflation: when did it rise or fall?
- USD/BRL vs. Selic: how do they move relative to each other?

### Tech stack (planned)

Python · requests · pandas · SQLite

### Roadmap

- [x] Define project goals and data sources
- [x] Create repository
- [ ] Extract: fetch the three series from the API
- [ ] Transform: clean, convert and combine
- [ ] Load: save to SQLite
- [ ] Add basic tests
- [ ] Add usage instructions and example analyses

### Getting started

_Coming soon._

### Data source

Data provided by the [Banco Central do Brasil (BCB)](https://dadosabertos.bcb.gov.br/) open data portal. Please check the portal for the current terms of use.

### License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file.

---

## 🇧🇷 Português

> 🚧 **Status: em desenvolvimento.** O projeto está sendo construído passo a passo. Este README será atualizado conforme cada etapa for concluída.

### Visão geral

Um **pipeline ETL (Extract, Transform, Load)** simples em Python, pensado para quem está começando. Ele coleta três indicadores econômicos brasileiros na API de dados abertos do Banco Central do Brasil (BCB) e os reúne em **uma única base, pronta para análise**.

| Indicador | Descrição |
|---|---|
| **USD/BRL** | Cotação do dólar em reais (diária) |
| **Selic** | Taxa básica de juros da economia brasileira |
| **IPCA** | Inflação ao consumidor (mensal) |

O período padrão é de **5 anos**.

### Por que este projeto?

As séries econômicas são publicadas em frequências diferentes (diária, mensal) e em formatos brutos de texto. Este pipeline cuida da parte trabalhosa — buscar, limpar e alinhar os dados — para você focar na análise.

### Como funciona

```
Extract  →  Transform  →  Load
  API BCB     limpar, converter,  tabela única
  (3 séries)  alinhar frequências (SQLite)
```

1. **Extract (extrair):** busca as três séries na API SGS do BCB.
2. **Transform (transformar):** converte textos em números e datas e alinha séries de frequências diferentes em uma só tabela.
3. **Load (carregar):** grava o resultado final para que qualquer pessoa possa consultar.

### Exemplos de análise (planejados)

- Inflação mês a mês: quando subiu ou caiu?
- Dólar × Selic: como se movimentam um em relação ao outro?

### Tecnologias (planejadas)

Python · requests · pandas · SQLite

### Roteiro

- [x] Definir objetivos e fontes de dados
- [x] Criar o repositório
- [ ] Extract: buscar as três séries na API
- [ ] Transform: limpar, converter e combinar
- [ ] Load: salvar em SQLite
- [ ] Adicionar testes básicos
- [ ] Adicionar instruções de uso e exemplos de análise

### Como começar

_Em breve._

### Fonte dos dados

Dados do portal de dados abertos do [Banco Central do Brasil (BCB)](https://dadosabertos.bcb.gov.br/). Consulte o portal para conferir os termos de uso atuais.

### Licença

Este projeto está sob a licença MIT — veja o arquivo [LICENSE](LICENSE).
