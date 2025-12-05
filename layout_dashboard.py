from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify 

# --- CONFIGURAÇÕES ---
CANCER_OPTIONS = [
    {'label': 'Câncer de Mama (Breast)', 'value': 'Breast Cancer'},
    {'label': 'Câncer de Pulmão (Lung)', 'value': 'Lung Cancer'},
    {'label': 'Leucemia (Leukemia)', 'value': 'Leukemia'},
    {'label': 'Melanoma (Pele)', 'value': 'Melanoma'},
    {'label': 'Câncer de Próstata', 'value': 'Prostate Cancer'},
    {'label': 'Tumor Cerebral', 'value': 'Brain Tumor'},
]

def draw_kpi_modern(title, id_value, color="blue", icon="tabler:chart-bar"):
    return dmc.Paper([
        dmc.Group([
            dmc.Stack([
                dmc.Text(title, c="dimmed", size="xs", fw=700, tt="uppercase"),
                html.H2(id=id_value, children="0", className=f"m-0 text-{color}", style={"fontSize": "2rem"})
            ], gap=0),
            dmc.ThemeIcon(DashIconify(icon=icon, width=22), size="lg", radius="xl", color=color, variant="light")
        ], justify="space-between", align="center")
    ], p="md", radius="md", shadow="sm", withBorder=True)

# --- LAYOUT LIMPO ---
layout = dmc.MantineProvider(
    forceColorScheme="light",
    theme={"primaryColor": "cyan", "fontFamily": "'Inter', sans-serif"},
    children=[
        # Fundo cinza claro para toda a página
        html.Div(style={"backgroundColor": "#f8f9fa", "minHeight": "100vh", "padding": "20px"}, children=[
            
            dmc.Container([
                # 1. CABEÇALHO SIMPLIFICADO
                dmc.Group([
                    dmc.ThemeIcon(DashIconify(icon="tabler:activity-heartbeat", width=30), size="xl", radius="md", color="cyan", variant="filled"),
                    dmc.Stack([
                        dmc.Text("ONCOLOGIA DIGITAL", fw=800, size="xl", lh=1, c="dark"),
                        dmc.Text("Painel de Monitoramento de Ensaios Clínicos", c="dimmed", size="sm")
                    ], gap=0)
                ], mb="xl"),

                # 2. BARRA DE CONTROLE (FILTROS)
                dmc.Paper([
                    dbc.Row([
                        dbc.Col([
                            dmc.Select(
                                id='dropdown-condicao',
                                label="Selecione a Patologia",
                                data=CANCER_OPTIONS,
                                value='Breast Cancer',
                                leftSection=DashIconify(icon="tabler:virus"),
                                clearable=False,
                                searchable=True
                            )
                        ], width=12, md=9),
                        dbc.Col([
                            dmc.Button("ATUALIZAR DADOS", id="btn-scan", fullWidth=True, size="md", leftSection=DashIconify(icon="tabler:refresh"), color="cyan", mt=24)
                        ], width=12, md=3)
                    ])
                ], p="lg", shadow="sm", radius="md", withBorder=True, mb="lg"),

                # 3. KPIS
                dbc.Row([
                    dbc.Col(draw_kpi_modern("Total de Ensaios", "kpi-total", "cyan", "tabler:flask"), width=12, md=6),
                    dbc.Col(draw_kpi_modern("Estudos Fase 3", "kpi-fase3", "teal", "tabler:checkbox"), width=12, md=6),
                ], className="g-3 mb-4"),

                # 4. GRÁFICOS PRINCIPAIS
                dbc.Row([
                    dbc.Col(
                        dmc.Paper([
                            dmc.Group([
                                DashIconify(icon="tabler:chart-pie", color="gray"),
                                dmc.Text("Distribuição por Fases", fw=700, size="sm")
                            ], mb="md"),
                            dcc.Graph(id='graph-stacked-phase', style={'height': '350px'}, config={'displayModeBar': False})
                        ], p="md", shadow="sm", radius="md", withBorder=True), 
                        width=12, lg=6, className="mb-3"
                    ),
                    dbc.Col(
                        dmc.Paper([
                            dmc.Group([
                                DashIconify(icon="tabler:layout-grid", color="gray"),
                                dmc.Text("Mapa de Hierarquia (Treemap)", fw=700, size="sm")
                            ], mb="md"),
                            dcc.Graph(id='graph-treemap', style={'height': '350px'}, config={'displayModeBar': False})
                        ], p="md", shadow="sm", radius="md", withBorder=True), 
                        width=12, lg=6, className="mb-3"
                    ),
                ], className="g-3"),

                # 5. MAPA GLOBAL
                dmc.Paper([
                    dmc.Group([
                        DashIconify(icon="tabler:world", color="gray"),
                        dmc.Text("Abrangência Global da Pesquisa", fw=700, size="sm")
                    ], mb="md"),
                    dcc.Graph(id='graph-map-geo', style={'height': '500px'})
                ], p="md", shadow="sm", radius="md", withBorder=True, mb="lg", mt="sm"),

                # 6. TABELA DE DADOS
                dmc.Paper([
                    dmc.Text("Detalhamento dos Ensaios", fw=700, size="sm", mb="md"),
                    dash_table.DataTable(
                        id='table-details',
                        columns=[
                            {"name": "ID", "id": "NCTId"},
                            {"name": "Título", "id": "Title"},
                            {"name": "Fase", "id": "Phase"},
                            {"name": "Status", "id": "Status"},
                        ],
                        page_size=10,
                        style_as_list_view=True,
                        cell_selectable=False,
                        style_header={'backgroundColor': '#f1f3f5', 'fontWeight': 'bold', 'borderBottom': '1px solid #dee2e6'},
                        style_cell={'padding': '12px', 'textAlign': 'left', 'fontFamily': 'Inter, sans-serif', 'fontSize': '13px'},
                        style_data_conditional=[
                            {'if': {'filter_query': '{Status} = "COMPLETED"'}, 'color': '#2b8a3e', 'fontWeight': 'bold'},
                            {'if': {'filter_query': '{Status} = "RECRUITING"'}, 'color': '#1864ab', 'fontWeight': 'bold'},
                            {'if': {'filter_query': '{Status} = "TERMINATED"'}, 'color': '#c92a2a', 'fontWeight': 'bold'},
                        ]
                    )
                ], p="md", shadow="sm", radius="md", withBorder=True, mb="xl")

            ], fluid=True, style={"maxWidth": "1400px"}) 
        ])
    ]
)