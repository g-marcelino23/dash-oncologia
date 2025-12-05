import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

# --- ÍCONES AUXILIARES ---
icon_info = DashIconify(icon="carbon:information", width=20)
icon_check = DashIconify(icon="carbon:checkmark-outline", width=20)
icon_alert = DashIconify(icon="carbon:warning", width=20)

# --- COMPONENTE AUXILIAR: STAT CARD ---
def create_stat_card(value, label, icon, color):
    return dmc.Paper(
        children=[
            dmc.Group([
                DashIconify(icon=icon, width=30, color=color),
                dmc.Text(value, fw=700, size="xl", c="dark")
            ]),
            dmc.Text(label, size="sm", c="dimmed", mt="xs")
        ],
        p="md", radius="md", withBorder=True, shadow="sm"
    )

# --- CONTEÚDO ---
content = dmc.Container([
    
    # 1. CABEÇALHO HERO
    dmc.Paper(
        children=[
            dmc.Group([
                DashIconify(icon="medical-icon:i-oncology", width=80, color="#228be6"),
                html.Div([
                    dmc.Text("Oncologia Digital", c="blue", size="sm", fw=700, tt="uppercase", lts=2),
                    dmc.Text(
                        "A Corrida pela Cura",
                        variant="gradient",
                        gradient={"from": "blue", "to": "cyan", "deg": 45},
                        style={"fontSize": "3rem", "fontWeight": 900, "lineHeight": 1.1, "marginBottom": "10px"}
                    ),
                    dmc.Text(
                        "Plataforma de Inteligência de Dados para Monitoramento de Ensaios Clínicos Globais.",
                        c="dimmed", size="lg", maw=600
                    )
                ])
            ], mb="xl", align="center"),
        ],
        shadow="xs", radius="lg", p="xl", withBorder=True, mb="xl", bg="gray.0"
    ),

    # 2. O PROBLEMA (CONTEXTO)
    dmc.Title("1. O Desafio da Pesquisa Médica", order=3, c="dark", mb="md"),
    dmc.Grid(
        gutter="md",
        mb="xl",
        children=[
            # Coluna da Esquerda: Citação Impactante
            dmc.GridCol(
                dmc.Blockquote(
                    "O 'Vale da Morte' na ciência refere-se à lacuna entre a descoberta básica e a aprovação clínica. Mais de 90% das drogas falham neste percurso devido à falta de eficácia ou segurança.",
                    cite="- National Institutes of Health (NIH)",
                    icon=icon_alert,
                    color="red",
                    radius="md",
                    h="100%" # Altura total
                ), span={"base": 12, "md": 7}
            ),
            # Coluna da Direita: Estatísticas Rápidas
            dmc.GridCol(
                dmc.Stack([
                    create_stat_card("12 Anos", "Tempo médio para aprovação de nova droga", "carbon:time", "blue"),
                    create_stat_card("US$ 2.6 Bi", "Custo médio de P&D por medicamento", "carbon:currency-dollar", "green"),
                    create_stat_card("10%", "Taxa de sucesso da Fase 1 até Aprovação", "carbon:chart-line-smooth", "orange"),
                ]), span={"base": 12, "md": 5}
            )
        ]
    ),

    dmc.Divider(mb="xl"),

    # 3. JORNADA DA APROVAÇÃO (TIMELINE)
    dmc.Title("2. Entendendo o Processo (Fases)", order=3, c="blue", mb="md"),
    dmc.Text(
        "Para navegar no dashboard, é crucial entender o ciclo de vida de um estudo clínico. Nossa ferramenta rastreia todas estas etapas:",
        c="dimmed", mb="lg"
    ),
    dmc.Paper(
        dmc.Timeline(
            active=2,
            bulletSize=40,
            lineWidth=3,
            children=[
                dmc.TimelineItem(
                    title="Fase 1: Segurança",
                    bullet=DashIconify(icon="carbon:chemistry", width=20),
                    children=[
                        dmc.Text("Foco: Avaliar segurança e dosagem em pequeno grupo (20-100).", size="sm", c="dimmed"),
                        dmc.Badge("Risco Alto", color="red", variant="light", mt="xs")
                    ]
                ),
                dmc.TimelineItem(
                    title="Fase 2: Eficácia",
                    bullet=DashIconify(icon="carbon:microscope", width=20),
                    children=[
                        dmc.Text("Foco: A droga funciona? Grupo médio (100-300).", size="sm", c="dimmed"),
                        dmc.Badge("Prova de Conceito", color="yellow", variant="light", mt="xs")
                    ]
                ),
                dmc.TimelineItem(
                    title="Fase 3: Confirmação",
                    bullet=DashIconify(icon="carbon:user-multiple", width=20),
                    lineVariant="dashed",
                    children=[
                        dmc.Text("Foco: Comparação com tratamento padrão em larga escala (1.000+).", size="sm", fw=700),
                        dmc.Badge("Decisivo", color="green", variant="filled", mt="xs")
                    ]
                ),
                dmc.TimelineItem(
                    title="Fase 4: Aprovação & Monitoramento",
                    bullet=DashIconify(icon="carbon:certificate-check", width=20),
                    children=[
                        dmc.Text("Foco: Farmacovigilância pós-comercialização.", size="sm", c="dimmed"),
                    ]
                ),
            ]
        ),
        p="xl", withBorder=True, radius="md", mb="xl", bg="white"
    ),

    # 4. SOBRE A FERRAMENTA (ARQUITETURA)
    dmc.Title("3. Metodologia e Fonte de Dados", order=3, c="dark", mb="md"),
    dmc.Paper(
        children=[
            dmc.Text(
                "Este dashboard conecta-se diretamente a bases de dados públicas para garantir transparência.", 
                mb="md"
            ),
            dmc.SimpleGrid(
                cols={"base": 1, "sm": 3},
                spacing="lg",
                children=[
                    dmc.Stack([
                        DashIconify(icon="carbon:data-base", width=30, color="gray"),
                        dmc.Text("Fonte: ClinicalTrials.gov", fw=700),
                        dmc.Text("Dados oficiais da Biblioteca Nacional de Medicina dos EUA.", size="sm", c="dimmed")
                    ]),
                    dmc.Stack([
                        DashIconify(icon="carbon:code", width=30, color="blue"),
                        dmc.Text("Processamento: Python", fw=700),
                        dmc.Text("Limpeza e padronização de nomes de países e status.", size="sm", c="dimmed")
                    ]),
                    dmc.Stack([
                        DashIconify(icon="carbon:dashboard", width=30, color="cyan"),
                        dmc.Text("Visualização: Dash", fw=700),
                        dmc.Text("Interface interativa para exploração ágil.", size="sm", c="dimmed")
                    ])
                ]
            )
        ],
        p="lg", withBorder=True, radius="md", mb="xl"
    ),

    # 5. GUIA DE LEITURA
    dmc.Title("4. Guia de Interpretação Visual", order=3, c="green", mb="md"),
    dmc.Accordion(
        variant="separated",
        radius="md",
        mb="xl",
        children=[
            dmc.AccordionItem([
                dmc.AccordionControl("📊 Barras: O Funil de Sobrevivência", icon=icon_info),
                dmc.AccordionPanel("Visualiza a quantidade de estudos em cada etapa. Barras decrescentes indicam a dificuldade de avançar da Fase 1 para a 3.")
            ], value="barras"),
            dmc.AccordionItem([
                dmc.AccordionControl("🌍 Mapa: Geopolítica da Ciência", icon=icon_info),
                dmc.AccordionPanel("Cores mais escuras indicam maior volume de pesquisa. Cinza indica ausência de dados públicos registrados.")
            ], value="mapa"),
            dmc.AccordionItem([
                dmc.AccordionControl("🔴🟢 Tabela: Status em Tempo Real", icon=icon_info),
                dmc.AccordionPanel("Use as cores para triagem rápida: Verde (Concluído), Azul (Recrutando) e Vermelho (Suspenso/Terminado).")
            ], value="tabela"),
        ]
    ),

    # 6. FOOTER / CTA
    dmc.Alert(
        title="Exploração Interativa",
        children="Acesse a aba 'Dashboard Analítico' acima para manipular estes dados em tempo real.",
        color="blue",
        variant="filled",
        icon=DashIconify(icon="carbon:arrow-right"),
        mb="xl"
    )

], fluid=True, py="xl", style={"maxWidth": "1200px"})

# --- EXPORTAÇÃO ---
layout = html.Div(content)