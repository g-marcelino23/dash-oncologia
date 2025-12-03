import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc # <--- IMPORTANTE

# Adicionamos dmc.styles.ALL para corrigir o estilo dos componentes novos
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.CERULEAN, dmc.styles.ALL], 
                suppress_callback_exceptions=True)

server = app.server