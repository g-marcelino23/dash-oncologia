from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

# DICA: Ao iniciar o app, use: app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

CANCER_OPTIONS = [
    {'label': 'Câncer de Mama (Breast)', 'value': 'Breast Cancer'},
    {'label': 'Câncer de Pulmão (Lung)', 'value': 'Lung Cancer'},
    {'label': 'Leucemia (Leukemia)', 'value': 'Leukemia'},
    {'label': 'Melanoma (Pele)', 'value': 'Melanoma'},
    {'label': 'Câncer de Próstata', 'value': 'Prostate Cancer'},
    {'label': 'Tumor Cerebral', 'value': 'Brain Tumor'},
]

# Componente de Cartão de KPI Reutilizável
def draw_kpi(title, id_value, color="primary", icon="📊"):
    return dbc.Card(
        dbc.CardBody([
            html.Div([
                html.H6(title, className="text-uppercase text-muted small fw-bold mb-2"),
                html.H2(id=id_value, children="0", className=f"display-4 fw-bold text-{color}")
            ])
        ]),
        className="h-100 shadow-sm border-0 border-start border-4 border-" + color
    )

layout = dbc.Container([
    # 1. Cabeçalho Principal
    dbc.Row([
        dbc.Col(html.H2("🔬 Monitoramento de Ensaios Clínicos", className="fw-bold text-dark"), width=12),
        dbc.Col(html.P("Visão global do progresso científico oncológico.", className="text-muted"), width=12),
        html.Hr(className="my-2")
    ], className="mb-4"),

    # 2. Barra de Controle (Card Flutuante)
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("SELECIONE A PATOLOGIA", className="small fw-bold text-secondary mb-1"),
                    dcc.Dropdown(
                        id='dropdown-condicao',
                        options=CANCER_OPTIONS,
                        value='Breast Cancer',
                        clearable=False,
                        className="mb-0"
                    )
                ], width=12, md=8),
                dbc.Col([
                    html.Label("AÇÃO", className="small fw-bold text-secondary mb-1"),
                    dbc.Button([html.Span("🔎"), " SCAN GLOBAL"], id="btn-scan", color="primary", className="w-100 fw-bold")
                ], width=12, md=4)
            ], className="align-items-end")
        ])
    ], className="shadow-sm border-0 mb-4 bg-white"),

    # 3. KPIs
    dbc.Row([
        dbc.Col(draw_kpi("Total de Ensaios Ativos", "kpi-total", "primary"), width=12, md=6),
        dbc.Col(draw_kpi("Em Fase 3 (Confirmação)", "kpi-fase3", "success"), width=12, md=6),
    ], className="g-4 mb-4"),

    # 4. Gráficos Linha 1
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("1. O Esforço Científico (Fases)", className="bg-transparent fw-bold border-0"),
                dbc.CardBody(dcc.Graph(id='graph-stacked-phase', style={'height': '350px'}))
            ], className="shadow-sm border-0 h-100"), 
            width=12, lg=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("2. Foco da Pesquisa", className="bg-transparent fw-bold border-0"),
                dbc.CardBody(dcc.Graph(id='graph-treemap', style={'height': '350px'}))
            ], className="shadow-sm border-0 h-100"), 
            width=12, lg=6
        ),
    ], className="g-4 mb-4"),

    # 5. Mapa Global
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("3. Liderança Global em Pesquisa", className="bg-transparent fw-bold border-0"),
                dbc.CardBody(dcc.Graph(id='graph-map-geo', style={'height': '450px'}))
            ], className="shadow-sm border-0"), 
            width=12
        ),
    ], className="mb-4"),

    # 6. Tabela Detalhada
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("4. Detalhamento dos Ensaios", className="bg-white fw-bold border-0"),
                dbc.CardBody(
                    dash_table.DataTable(
                        id='table-details',
                        columns=[
                            {"name": "ID", "id": "NCTId"},
                            {"name": "Título", "id": "Title"},
                            {"name": "Fase", "id": "Phase"},
                            {"name": "Status", "id": "Status"},
                        ],
                        page_size=10,
                        style_as_list_view=True,  # Estilo mais limpo (sem bordas verticais)
                        style_header={'backgroundColor': 'white', 'fontWeight': 'bold', 'borderBottom': '2px solid #eee'},
                        style_cell={'padding': '12px', 'fontFamily': 'sans-serif', 'fontSize': '14px'},
                        style_data_conditional=[
                            {'if': {'filter_query': '{Status} = "COMPLETED"'}, 'color': '#198754', 'fontWeight': 'bold'},
                            {'if': {'filter_query': '{Status} = "RECRUITING"'}, 'color': '#0d6efd', 'fontWeight': 'bold'},
                            {'if': {'filter_query': '{Status} = "TERMINATED"'}, 'color': '#dc3545', 'fontWeight': 'bold'},
                        ]
                    )
                )
            ], className="shadow-sm border-0"), 
            width=12
        )
    ])

], fluid=True, className="bg-light p-4", style={"minHeight": "100vh"})