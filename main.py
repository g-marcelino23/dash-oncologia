import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd

# Importa os módulos locais
from app import app
from data_handler import fetch_oncology_data
import layout_presentation
import layout_dashboard

# --- LAYOUT PRINCIPAL (Modernizado com DMC 2.4.0) ---
app.layout = dmc.MantineProvider(
    html.Div([
        
        # 1. CABEÇALHO CENTRALIZADO
        dmc.Paper(
            children=[
                dmc.Center(
                    dmc.Stack(
                        children=[
                            dmc.Group([
                                DashIconify(icon="medical-icon:i-oncology", width=40, color="#228be6"),
                                dmc.Title("ONCOLOGIA DIGITAL", order=2, c="blue", fw=900),
                            ], justify="center"),
                            
                            dmc.Text("MISSÃO CURA // Plataforma de Inteligência de Dados", c="dimmed", size="sm")
                        ],
                        gap="xs",
                        style={"textAlign": "center"}
                    )
                ),
            ],
            py="md", shadow="xs", withBorder=True, mb="lg"
        ),

        # 2. NAVEGAÇÃO (ABAS)
        dmc.Container([
            dmc.Tabs(
                id="tabs-main",
                value="tab-presentation",
                variant="pills",
                color="cyan",
                children=[
                    dmc.TabsList(
                        [
                            dmc.TabsTab(
                                "Apresentação", 
                                value="tab-presentation", 
                                leftSection=DashIconify(icon="carbon:presentation-file")
                            ),
                            dmc.TabsTab(
                                "Dashboard Analítico", 
                                value="tab-dashboard", 
                                leftSection=DashIconify(icon="carbon:chart-multitype")
                            ),
                        ],
                        justify="center" 
                    ),
                ],
                mb="xl"
            ),
            
            # 3. ÁREA DE CONTEÚDO
            html.Div(id='tabs-content')
            
        ], fluid=True, size="xl")
        
    ], style={"backgroundColor": "#f8f9fa", "minHeight": "100vh"})
)

# --- CALLBACKS ---

# 1. Navegação entre Abas
@app.callback(Output('tabs-content', 'children'),
              Input('tabs-main', 'value'))
def render_content(tab):
    if tab == 'tab-presentation':
        return layout_presentation.layout
    elif tab == 'tab-dashboard':
        return layout_dashboard.layout

# 2. Lógica do Dashboard
@app.callback(
    [Output('kpi-total', 'children'),
     Output('kpi-fase3', 'children'),
     Output('graph-stacked-phase', 'figure'),
     Output('graph-treemap', 'figure'), # ID mantido para compatibilidade, mas gerará Donut
     Output('graph-map-geo', 'figure'),
     Output('table-details', 'data'),
     Output('table-details', 'columns')],
    [Input('dropdown-condicao', 'value'), 
     Input('btn-scan', 'n_clicks')],
    [State('dropdown-condicao', 'value')]
)
def update_dashboard(selected_condition_input, n_clicks, condition_state):
    target_condition = selected_condition_input if selected_condition_input else "Cancer"
    
    # 1. Busca os dados
    df = fetch_oncology_data(target_condition)
    
    if df.empty:
        return "0", "0", go.Figure(), go.Figure(), go.Figure(), [], []
    
    # --- TRATAMENTO DE DADOS (CRUCIAL) ---
    
    # A. Corrige Status para Maiúsculo
    if 'Status' in df.columns:
        df['Status'] = df['Status'].str.upper()

    # B. Corrige Nomes de Países
    mapa_nomes = {
        "USA": "United States",
        "United States of America": "United States",
        "UK": "United Kingdom",
        "South Korea": "Korea, Rep.",
        "Korea, Republic of": "Korea, Rep.",
        "Russia": "Russian Federation",
        "Iran": "Iran, Islamic Rep.",
        "Vietnam": "Viet Nam",
        "Taiwan": "Taiwan, Province of China",
        "China": "China"
    }
    col_pais = 'Location' if 'Location' in df.columns else 'Country'
    if col_pais in df.columns:
        df[col_pais] = df[col_pais].replace(mapa_nomes)

    # C. Limpeza Robusta das Fases
    def limpar_fase(val):
        s = str(val).lower()
        if '4' in s or 'iv' in s: return 'Fase 4 (Pós-Aprovação)'
        if '3' in s or 'iii' in s: return 'Fase 3 (Confirmação)'
        if '2' in s or 'ii' in s: return 'Fase 2 (Eficácia)'
        if '1' in s or 'i' in s: return 'Fase 1 (Segurança)'
        return 'Outros/Indefinido'

    df['Phase_Clean'] = df['Phase'].apply(limpar_fase)

    # --- CÁLCULOS E GRÁFICOS ---
    
    # KPIs
    total = len(df)
    fase3 = len(df[df['Phase_Clean'] == 'Fase 3 (Confirmação)'])
    
    # Gráfico 1: Barras (Fases) - FIX: Reindex para garantir Fase 4
    ordem_fases = ['Fase 1 (Segurança)', 'Fase 2 (Eficácia)', 'Fase 3 (Confirmação)', 'Fase 4 (Pós-Aprovação)']
    
    # O .reindex garante que todas as fases existam, mesmo com contagem 0
    funnel_data = df['Phase_Clean'].value_counts().reindex(ordem_fases, fill_value=0).reset_index()
    funnel_data.columns = ['Fase', 'Quantidade']
    
    fig_bar = px.bar(funnel_data, y='Fase', x='Quantidade', orientation='h',
                     category_orders={'Fase': ordem_fases},
                     color='Quantidade', color_continuous_scale=px.colors.sequential.Teal)
    fig_bar.update_layout(template="plotly_white", margin={"r":10,"t":10,"l":10,"b":10}, yaxis={'categoryorder':'array', 'categoryarray': ordem_fases})

    # Gráfico 2: DONUT CHART (Restaurado no lugar do Treemap)
    # Agrupa dados pequenos em "Outros" para limpar o gráfico
    intervention_counts = df['InterventionType'].value_counts()
    if len(intervention_counts) > 5:
        top_5 = intervention_counts.head(5)
        outros = pd.Series([intervention_counts.iloc[5:].sum()], index=['Outros'])
        intervention_counts = pd.concat([top_5, outros])
    
    donut_data = intervention_counts.reset_index()
    donut_data.columns = ['Tipo', 'Quantidade']

    fig_donut = px.pie(donut_data, names='Tipo', values='Quantidade', hole=0.6, 
                       color_discrete_sequence=px.colors.sequential.Blues_r)
    fig_donut.update_layout(template="plotly_white", margin={"t":0, "l":0, "r":0, "b":0}, showlegend=True)

    # Gráfico 3: Mapa
    df_countries = df[col_pais].value_counts().reset_index()
    df_countries.columns = ['Country', 'Count']
    
    fig_map = px.choropleth(df_countries, locations='Country', color='Count',
                            locationmode='country names', 
                            color_continuous_scale=px.colors.sequential.Teal)
    
    fig_map.update_geos(
        visible=True, 
        showcountries=True, 
        countrycolor="#d1d1d1",
        showland=True, 
        landcolor="#f8f9fa",
        fitbounds="locations"
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, template="plotly_white")

    # Tabela
    columns = [
        {"name": "ID", "id": "NCTId"},
        {"name": "Título", "id": "Title"},
        {"name": "Fase", "id": "Phase"},
        {"name": "Status", "id": "Status"},
    ]
    table_data = df[['NCTId', 'Title', 'Phase', 'Status']].to_dict('records')

    # Retorna fig_donut no lugar onde estava fig_treemap
    return str(total), str(fase3), fig_bar, fig_donut, fig_map, table_data, columns

# --- RODAR O APP ---
if __name__ == '__main__':
    app.run(debug=False, port=8050)