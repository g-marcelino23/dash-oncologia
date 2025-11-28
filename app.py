# --- Em app.py ---
import dash
import dash_bootstrap_components as dbc

# MUDANÇA AQUI: De FLATLY para CERULEAN (Visual limpo/clínico)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN], suppress_callback_exceptions=True)
server = app.server