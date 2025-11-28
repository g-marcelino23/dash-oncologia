from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    # --- CABEÇALHO: O TEMA ---
    dbc.Row([
        dbc.Col(html.Div([
            html.H1("🧬 Oncologia Digital: A Corrida pela Cura", className="display-4 text-primary mb-1"),
            html.P("Projeto NP3: Visualização de Dados e Storytelling em Ensaios Clínicos.", className="lead text-muted"),
            html.Hr(className="my-3"),
            html.P("Esta ferramenta oferece uma visão em tempo real sobre o esforço global na pesquisa contra o câncer, com foco na transparência e no Funil de Falhas.", className="text-secondary")
        ], className="h-100 p-5 bg-white border rounded-3 shadow-sm"), width=12) 
    ], className="py-4"),

    # --- SEÇÃO 1: O DESAFIO E O FUNIL DE FALHAS ---
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4("1. O Desafio Científico: O Funil de Falhas", className="card-title text-danger")),
            dbc.CardBody([
                html.P(
                    "O desenvolvimento de um novo tratamento oncológico é um processo longo, caro e de altíssimo risco. "
                    "Historicamente, a taxa de sucesso de um medicamento que entra na Fase 1 e chega ao mercado é inferior a **10%**.", className="card-text fw-bold"
                ),
                html.P(
                    "Este projeto nasceu para dar visibilidade a esse risco. Os dados, isolados, não contam a história; "
                    "o desafio é transformar a 'mortalidade' dos estudos em uma **visualização intuitiva** (Gráfico de Barras), "
                    "mostrando o esforço que 'encolhe' de fase para fase.", className="card-text"
                ),
            ])
        ], color="light", outline=True, className="h-100"), width=6),
        
        # O que é Ensaio Clínico
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4("Glossário: Ensaios e Fases", className="card-title text-info")),
            dbc.CardBody([
                html.P(
                    html.Strong("Ensaio Clínico:"), " Estudo de pesquisa que avalia a segurança e eficácia de novos tratamentos em pacientes. É a etapa final antes da aprovação regulatória."
                ),
                html.Ul([
                    html.Li(html.Strong("Fase 1 (Segurança):"), " Testes iniciais com poucos pacientes. Foco em dosagem e efeitos colaterais."),
                    html.Li(html.Strong("Fase 3 (Confirmação):"), " Testes em larga escala (milhares de pacientes). Foco em provar que o tratamento é **superior** ao padrão atual."),
                ]),
            ])
        ], color="light", outline=True, className="h-100"), width=6),
    ], className="mb-4"),

    # --- SEÇÃO 2: A SOLUÇÃO EM DATAVIZ E ARQUITETURA ---
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4("2. A Solução: Visualização Autoexplicativa", className="card-title text-success")),
            dbc.CardBody([
                html.P(
                    "Nosso design prioriza a **clareza imediata (UX)**. Cada gráfico foi escolhido para ter um entendimento rápido, sem depender do conhecimento científico do usuário.", className="card-text fw-bold"
                ),
                html.Ul([
                    html.Li(html.Strong("Gráfico de Barras (Esforço Científico):"), " Substitui o Funil complexo por uma contagem simples, que revela a 'mortalidade' do risco de forma gráfica."),
                    html.Li(html.Strong("Donut Chart (Foco da Pesquisa):"), " Mostra o percentual de intervenções (Droga, Cirurgia, etc.), direcionando o foco estratégico."),
                    html.Li(html.Strong("Mapa Coroplético (Liderança Global):"), " Usa o preenchimento de cor do país (e não bolinhas) para mostrar o volume de pesquisa de forma intuitiva, corrigindo o problema de proporção."),
                    html.Li(html.Strong("Tabela Condicional:"), " Cores na tabela indicam o status do estudo (Verde para 'Completo', Vermelho para 'Terminado'), agilizando a auditoria dos dados."),
                ]),
            ])
        ], color="light", outline=True, className="h-100"), width=6),

        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4("3. Arquitetura e Rastreabilidade (O Rigor Técnico)", className="card-title text-primary")),
            dbc.CardBody([
                html.P(
                    html.Strong("Fonte de Dados:"), " API Pública do ClinicalTrials.gov (NIH/EUA). Garante que a informação é oficial e em tempo real."
                ),
                html.P(
                    html.Strong("Tecnologias:"), " Construído em **Python Dash**, usando o framework **Plotly** para visualização e **Pandas** para a limpeza e transformação (ETL) dos dados brutos recebidos da API."
                ),
                html.P(
                    html.Strong("Design Clínico:"), " Implementação do tema **Cerulean (Bootstrap)** para estética limpa e hospitalar, reforçando a seriedade do tema."
                ),
            ])
        ], color="light", outline=True, className="h-100"), width=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Alert(
            html.P(["Navegue para a aba ", html.Strong("🧪 DASHBOARD"), " para uma demonstração da aplicação em tempo real e em diferentes patologias."]), 
            color="primary"), width=12)
    ])
], fluid=True, style={'minHeight': '80vh'})