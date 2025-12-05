import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc 

app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.CERULEAN, dmc.styles.ALL], 
                suppress_callback_exceptions=True)

# Obrigatório para o Render
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)