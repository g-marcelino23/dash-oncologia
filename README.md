# 🧬 Projeto NP3: Oncologia Digital - A Corrida pela Cura

## 🎯 Objetivo do Projeto

Este projeto consiste no desenvolvimento de uma aplicação web interativa (dashboard) focada em **Visualização de Dados Científicos**. O objetivo é transformar o ciclo complexo de pesquisa clínica em Oncologia em uma narrativa visual clara, permitindo o rastreamento em tempo real do progresso global contra o câncer.

---

## 💡 Storytelling & Diferenciais (Nota Máxima)

A narrativa central do projeto é o **"Funil de Falhas"**. O dashboard guia o usuário na descoberta da taxa de insucesso dos tratamentos, que é um dos maiores desafios da pesquisa moderna.

| Funcionalidade | Tipo de Gráfico | Requisito que Cumpre |
| :--- | :--- | :--- |
| **Funil da Cura** | Gráfico de Funil | **Inovação/Storytelling:** Mede a taxa de sucesso (Fase 1 → Fase 3). |
| **Mapeamento Científico** | Mapa-Múndi (Mapbox) | **Recurso Dinâmico/UX:** Localiza os hubs de pesquisa mais ativos. |
| **Análise de Intervenção** | Gráfico de Sunburst | **Complexidade Técnica:** Detalha os tipos de intervenção (drogas vs. cirurgia) por tipo de câncer. |
| **Integração de Dados** | API REST | **API:** Conexão direta e robusta com a base ClinicalTrials.gov. |

---

## 🛠️ Tecnologias Utilizadas

O projeto é baseado integralmente no ecossistema Python.

| Ferramenta | Uso |
| :--- | :--- |
| **🐍 Python 3.x** | Linguagem principal. |
| **⚛️ Dash Plotly** | Framework para o desenvolvimento da aplicação web. |
| **📊 Plotly Express** | Motor de renderização dos gráficos (3D, Funil, Sunburst). |
| **🐼 Pandas** | ETL (Extração, Transformação e Carga) e manipulação do JSON complexo da API. |
| **🌐 requests** | Conexão e busca de dados em tempo real da API. |
| **🔗 dash-bootstrap-components** | Layout moderno e responsivo (UX). |

---

## ⚙️ Configuração e Execução

Para rodar este projeto localmente, siga os passos abaixo.

### Pré-requisitos

Certifique-se de ter o [Python 3.x](https://www.python.org/downloads/) e o `pip` instalados.

### 1. Criar e Ativar o Ambiente Virtual

Abra o terminal na pasta raiz do projeto e execute:

```bash
# Cria o ambiente virtual
python -m venv venv

# Ativa o ambiente (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# OU (Linux/macOS)
source venv/bin/activate
