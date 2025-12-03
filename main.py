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
                            # FIX: 'justify' substitui 'position'
                            dmc.Group([
                                DashIconify(icon="medical-icon:i-oncology", width=40, color="#228be6"),
                                # FIX: 'c' substitui 'color'
                                dmc.Title("ONCOLOGIA DIGITAL", order=2, c="blue", fw=900),
                            ], justify="center"),
                            
                            dmc.Text("MISSÃO CURA // Plataforma de Inteligência de Dados", c="dimmed", size="sm")
                        ],
                        gap="xs", # FIX: 'gap' substitui 'spacing'
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
                    # FIX: 'justify' substitui 'position'
                    dmc.TabsList(
                        [
                            # FIX CRÍTICO: 'TabsTab' substitui 'Tab'
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
    
    # KPIs
    total = len(df)
    fase3 = len(df[df['Phase'].str.contains("Fase 3", na=False)])
    
    # Gráficos
    funnel_data = df['Phase'].value_counts().reindex(['Fase 1 (Segurança)', 'Fase 2 (Eficácia)', 'Fase 3 (Confirmação)', 'Aprovado/Fase 4'], fill_value=0).reset_index()
    funnel_data.columns = ['Fase', 'Quantidade']
    
    fig_bar = px.bar(funnel_data, y='Fase', x='Quantidade', orientation='h',
                     title=f"1. O Esforço Científico: {target_condition}",
                     color='Quantidade', color_continuous_scale=px.colors.sequential.Teal)
    fig_bar.update_layout(template="plotly_white", margin={"r":10,"t":40,"l":10,"b":10})

    fig_donut = px.pie(df, names='InterventionType', hole=0.6, 
                       title="2. Foco da Pesquisa",
                       color_discrete_sequence=px.colors.sequential.Blues_r)
    fig_donut.update_layout(template="plotly_white")

    df_countries = df['Location'].value_counts().reset_index()
    df_countries.columns = ['Country', 'Count']
    
    fig_map = px.choropleth(df_countries, locations='Country', color='Count',
                            locationmode='country names', 
                            color_continuous_scale=px.colors.sequential.Teal,
                            title="3. Liderança Global")
    fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, template="plotly_white")

    # Tabela
    columns = [
        {"name": "ID", "id": "NCTId"},
        {"name": "Título", "id": "Title"},
        {"name": "Fase", "id": "Phase"},
        {"name": "Status", "id": "Status"},
    ]
    table_data = df[['NCTId', 'Title', 'Phase', 'Status']].to_dict('records')

    return str(total), str(fase3), fig_bar, fig_donut, fig_map, table_data, columns

# --- RODAR O APP ---
if __name__ == '__main__':
    app.run(debug=False, port=8050)