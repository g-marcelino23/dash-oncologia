from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

# Opções do Dropdown (Em inglês para a API)
CANCER_OPTIONS = [
    {'label': 'Câncer de Mama (Breast)', 'value': 'Breast Cancer'},
    {'label': 'Câncer de Pulmão (Lung)', 'value': 'Lung Cancer'},
    {'label': 'Leucemia (Leukemia)', 'value': 'Leukemia'},
    {'label': 'Melanoma (Pele)', 'value': 'Melanoma'},
    {'label': 'Câncer de Próstata', 'value': 'Prostate Cancer'},
    {'label': 'Tumor Cerebral', 'value': 'Brain Tumor'},
]

layout = dbc.Container([
    # Linha de Filtros
    dbc.Row([
        dbc.Col([
            html.Label("SELECIONE A PATOLOGIA:", className="fw-bold text-primary"),
            dcc.Dropdown(
                id='dropdown-condicao', 
                options=CANCER_OPTIONS,
                value='Breast Cancer', 
                clearable=False
            )
        ], width=8),
        dbc.Col([
            html.Label("AÇÃO:", className="fw-bold text-primary"),
            dbc.Button("SCAN GLOBAL 🔎", id="btn-scan", color="primary", className="w-100")
        ], width=4)
    ], className="my-4 p-3 bg-light rounded"),

    # Linha de KPIs
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Total de Ensaios Ativos", className="text-muted"),
            html.H2(id="kpi-total", children="0", className="text-primary")
        ]), className="h-100"), width=6),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Em Fase 3 (Confirmação)", className="text-muted"),
            html.H2(id="kpi-fase3", children="0", className="text-success")
        ]), className="h-100"), width=6),
    ], className="mb-4"),

    # Linha Gráficos 1 (Barra Horizontal + Donut)
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("1. O Esforço Científico (Contagem por Fase)"),
                dbc.CardBody(dcc.Graph(id='graph-stacked-phase', style={'height': '350px'})) 
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("2. Foco da Pesquisa (Intervenção e Tipo)"),
                dbc.CardBody(dcc.Graph(id='graph-treemap', style={'height': '350px'})) 
            ])
        ], width=6),
    ], className="mb-4"),

    # Linha Gráficos 2 (Mapa Coroplético + Tabela)
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("3. Liderança Global em Pesquisa"),
                dbc.CardBody(dcc.Graph(id='graph-map-geo', style={'height': '400px'})) 
            ])
        ], width=12, className="mb-4"),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("4. Detalhes dos Ensaios (Status Condicional)"),
                dbc.CardBody(
                    dash_table.DataTable(
                        id='table-details', 
                        columns=[
                            {"name": "ID", "id": "NCTId"},
                            {"name": "Título", "id": "Title"},
                            {"name": "Fase", "id": "Phase"},
                            {"name": "Status", "id": "Status"},
                        ],
                        page_size=5,
                        # ESTILOS DE COR (UX Autoexplicativo)
                        style_data_conditional=[
                            {'if': {'filter_query': '{Status} = "COMPLETED"'}, 'backgroundColor': '#d4edda', 'color': '#155724'},
                            {'if': {'filter_query': '{Status} = "RECRUITING"'}, 'backgroundColor': '#ffe6cc', 'color': '#856404'},
                            {'if': {'filter_query': '{Status} = "TERMINATED"'}, 'backgroundColor': '#f8d7da', 'color': '#721c24'},
                        ],
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '10px'},
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
                    )
                )
            ])
        ], width=12)
    ])
], fluid=True)