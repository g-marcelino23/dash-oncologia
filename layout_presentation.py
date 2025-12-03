import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

# --- ICONES AUXILIARES ---
icon_info = DashIconify(icon="carbon:information", width=20)
icon_check = DashIconify(icon="carbon:checkmark-outline", width=20)

# --- CONTEÚDO ---
content = dmc.Container([
    
    # 1. CABEÇALHO HERO (Impacto Visual)
    dmc.Paper(
        children=[
            dmc.Group([
                DashIconify(icon="medical-icon:i-oncology", width=60, color="#228be6"),
                html.Div([
                    dmc.Text(
                        "Oncologia Digital: A Corrida pela Cura",
                        variant="gradient",
                        gradient={"from": "blue", "to": "cyan", "deg": 45},
                        style={"fontSize": "2.5rem", "fontWeight": 900, "lineHeight": 1.1}
                    ),
                    dmc.Text(
                        "Desmistificando a Complexidade dos Ensaios Clínicos Globais.",
                        c="dimmed", size="lg", mt="xs"
                    )
                ])
            ], mb="xl", align="center"),
            
            dmc.Divider(label="CONTEXTO CIENTÍFICO", labelPosition="center", mb="lg"),
            
            # BLOCO DE DESTAQUE (O Problema)
            dmc.Blockquote(
                "O desenvolvimento de uma nova droga oncológica leva em média 12 anos e custa mais de 2 bilhões de dólares. Mais de 90% das drogas falham antes de chegar ao mercado.",
                cite="- The 'Valley of Death' in Drug Development",
                icon=DashIconify(icon="carbon:warning-alt-filled", width=30),
                color="red",
                radius="md",
                mb="xl"
            ),
        ],
        shadow="xs", radius="lg", p="xl", withBorder=True, mb="xl"
    ),

    # 2. SEÇÃO EDUCACIONAL: O QUE SÃO AS FASES? (Timeline)
    dmc.Title("1. A Jornada da Aprovação (Fases)", order=3, c="blue", mb="md"),
    dmc.Paper(
        dmc.Timeline(
            active=1, # Indica que estamos "observando" o processo
            bulletSize=30,
            lineWidth=2,
            children=[
                # FASE 1
                dmc.TimelineItem(
                    title="Fase 1: Segurança (O Início)",
                    bullet=DashIconify(icon="carbon:chemistry", width=15),
                    children=[
                        dmc.Text("Teste em um pequeno grupo (20-80 pessoas).", size="sm", c="dimmed"),
                        dmc.Text("Objetivo: Descobrir se a droga é segura e qual a dose correta.", size="sm", fw=500),
                    ]
                ),
                # FASE 2
                dmc.TimelineItem(
                    title="Fase 2: Eficácia (A Prova)",
                    bullet=DashIconify(icon="carbon:microscope", width=15),
                    children=[
                        dmc.Text("Teste em grupo médio (100-300 pessoas).", size="sm", c="dimmed"),
                        dmc.Text("Objetivo: A droga funciona? Existem efeitos colaterais?", size="sm", fw=500),
                    ]
                ),
                # FASE 3
                dmc.TimelineItem(
                    title="Fase 3: Confirmação (O Grande Teste)",
                    bullet=DashIconify(icon="carbon:user-multiple", width=15),
                    lineVariant="dashed",
                    children=[
                        dmc.Text("Milhares de pacientes em vários países.", size="sm", c="dimmed"),
                        dmc.Text("Objetivo: Comparar com o tratamento padrão atual. É melhor do que o que já existe?", size="sm", fw=700, c="blue"),
                    ]
                ),
                # FASE 4 / APROVAÇÃO
                dmc.TimelineItem(
                    title="Aprovação Regulatória (FDA/Anvisa)",
                    bullet=DashIconify(icon="carbon:certificate-check", width=15),
                    children=[
                        dmc.Text("O medicamento chega ao mercado e continua sendo monitorado.", size="sm", c="dimmed"),
                    ]
                ),
            ]
        ),
        p="xl", withBorder=True, radius="md", mb="xl"
    ),

    # 3. SEÇÃO TÉCNICA: COMO LER O DASHBOARD (Accordion)
    dmc.Title("2. Guia de Leitura dos Dados", order=3, c="green", mb="md"),
    dmc.Accordion(
        variant="separated",
        radius="md",
        mb="xl",
        children=[
            dmc.AccordionItem(
                [
                    dmc.AccordionControl("📊 Gráfico de Barras: O Funil de Sobrevivência", icon=icon_info),
                    dmc.AccordionPanel(
                        "Este gráfico mostra a 'mortalidade' dos estudos. Você verá muitas barras grandes na Fase 1 e barras pequenas na Fase 3. Isso visualiza o risco financeiro e científico diminuindo conforme o funil avança."
                    ),
                ],
                value="info-barras"
            ),
            dmc.AccordionItem(
                [
                    dmc.AccordionControl("🌍 Mapa Global: Onde a Ciência Acontece", icon=icon_info),
                    dmc.AccordionPanel(
                        "Identifica os países líderes em pesquisa. Note a concentração nos EUA e Europa, mas observe o crescimento da China e Brasil em ensaios clínicos recentes."
                    ),
                ],
                value="info-mapa"
            ),
            dmc.AccordionItem(
                [
                    dmc.AccordionControl("🍩 Donut Chart: Estratégia Terapêutica", icon=icon_info),
                    dmc.AccordionPanel(
                        "Mostra O QUE está sendo testado. É uma nova Droga? Radiação? Genética? Isso revela a tendência tecnológica da indústria farmacêutica."
                    ),
                ],
                value="info-donut"
            ),
        ]
    ),

    # 4. CALL TO ACTION FINAL
    dmc.Alert(
        title="Pronto para explorar?",
        children="Agora que você entende o processo, acesse a aba 'Dashboard Analítico' para ver esses dados em tempo real.",
        color="blue",
        variant="light",
        icon=DashIconify(icon="carbon:arrow-right")
    )

], fluid=True, py="xl")

# --- EXPORTAÇÃO (CRÍTICO PARA O MAIN.PY) ---
layout = dmc.MantineProvider(content)