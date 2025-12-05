import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc 

# 1. ATIVA O REACT 18 (Obrigatório para DMC novo funcionar)
dash._dash_renderer._set_react_version("18.2.0")

# 2. CARREGA O CSS DO MANTINE (Obrigatório, senão fica invisível)
stylesheets = [
    dbc.themes.CERULEAN,
    "https://unpkg.com/@mantine/core@7.10.0/styles.css",
    "https://unpkg.com/@mantine/dates@7.10.0/styles.css"
]

app = dash.Dash(__name__, 
                external_stylesheets=stylesheets, 
                suppress_callback_exceptions=True)

server = app.server

# 3. SEU LAYOUT
app.layout = dmc.MantineProvider(
    children=[
        # --- COLE O SEU CONTEÚDO AQUI DENTRO ---
        # (Seus gráficos, dmc.Container, etc)
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)