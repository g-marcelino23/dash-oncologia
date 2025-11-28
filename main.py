import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import random
from datetime import datetime

# Importa os módulos que criamos
from app import app
from data_handler import fetch_oncology_data # Função de busca da API
import layout_presentation
import layout_dashboard

# --- LAYOUT PRINCIPAL (Navegação) ---
app.layout = html.Div([
    # Barra de Navegação Simples
    dbc.NavbarSimple(
        brand="ONCOLOGIA DIGITAL // MISSÃO CURA",
        brand_href="#",
        color="primary",
        dark=True,
        className="mb-0"
    ),
    
    # Abas
    dcc.Tabs(id="tabs-main", value='tab-presentation', children=[
        dcc.Tab(label='📋 APRESENTAÇÃO', value='tab-presentation', className="p-2"),
        dcc.Tab(label='🧪 DASHBOARD', value='tab-dashboard', className="p-2"),
    ]),
    
    # Área onde o conteúdo muda
    html.Div(id='tabs-content')
])

# --- CALLBACKS ---

# 1. Navegação entre Abas
@app.callback(Output('tabs-content', 'children'),
              Input('tabs-main', 'value'))
def render_content(tab):
    # CORREÇÃO: Usar 'tab-presentation' para corresponder ao dcc.Tab
    if tab == 'tab-presentation':
        return layout_presentation.layout
    elif tab == 'tab-dashboard':
        return layout_dashboard.layout


# 2. Lógica do Dashboard (API → Processamento → Gráficos)
@app.callback(
    [Output('kpi-total', 'children'),
     Output('kpi-fase3', 'children'),
     Output('graph-stacked-phase', 'figure'),
     Output('graph-treemap', 'figure'),
     Output('graph-map-geo', 'figure'),
     Output('table-details', 'data'),
     Output('table-details', 'columns')],
    [Input('dropdown-condicao', 'value'), 
     Input('btn-scan', 'n_clicks')],
    [State('dropdown-condicao', 'value')]
)
def update_dashboard(selected_condition_input, n_clicks, condition_state):
    target_condition = selected_condition_input if selected_condition_input else "Cancer"
    df = fetch_oncology_data(target_condition)
    
    if df.empty:
        return "0", "0", go.Figure(), go.Figure(), go.Figure(), [], []
    
    # --- CÁLCULOS E KPIS (Igual) ---
    total = len(df)
    fase3 = len(df[df['Phase'].str.contains("Fase 3")])
    
    # --- GERAÇÃO DOS GRÁFICOS (CORES CLÍNICAS) ---
    
    funnel_data = df['Phase'].value_counts().reindex(['Fase 1 (Segurança)', 'Fase 2 (Eficácia)', 'Fase 3 (Confirmação)', 'Aprovado/Fase 4'], fill_value=0).reset_index()
    funnel_data.columns = ['Fase', 'Quantidade']
    
    # Gráfico 1: Barras Horizontais (Funil Simplificado)
    fig_bar = px.bar(funnel_data, y='Fase', x='Quantidade', orientation='h',
                     title=f"1. O Esforço Científico: {target_condition}",
                     # MUDANÇA: Usando cores azuis suaves para o tema clínico
                     color='Quantidade',
                     color_continuous_scale=px.colors.sequential.Cividis, 
                     labels={'Fase': 'Fase Clínica', 'Quantidade': 'Total de Ensaios'})
    
    # Gráfico 2: Donut Chart (Foco da Pesquisa)
    fig_donut = px.pie(df, names='InterventionType', hole=0.6, 
                       title="2. Foco da Pesquisa (Tipo de Intervenção)",
                       # MUDANÇA: Usando cores Primárias/Azuis
                       color_discrete_sequence=px.colors.sequential.Blues_r) 

    # Gráfico 3: Mapa Coroplético (Liderança Global)
    df_countries = df['Location'].value_counts().reset_index()
    df_countries.columns = ['Country', 'Count']
    
    fig_map = px.choropleth(df_countries, locations='Country', color='Count',
                            locationmode='country names', 
                            # MUDANÇA: Usando cores suaves (Cividis/Teal)
                            color_continuous_scale=px.colors.sequential.Teal,
                            title="3. Liderança Global em Ensaios")
    fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

    # --- TABELA DE DETALHES (Igual) ---
    columns = [
        {"name": "ID", "id": "NCTId"},
        {"name": "Título", "id": "Title"},
        {"name": "Fase", "id": "Phase"},
        {"name": "Status", "id": "Status"},
    ]
    table_data = df[['NCTId', 'Title', 'Phase', 'Status']].to_dict('records')

    # --- RETORNO DOS RESULTADOS ---
    return str(total), str(fase3), fig_bar, fig_donut, fig_map, table_data, columns

# --- RODAR O APP ---
if __name__ == '__main__':
    app.run(debug=False, port=8050)