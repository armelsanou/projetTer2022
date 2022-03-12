import dash
import dash_bootstrap_components as dbc
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
#server = app.serverapp.config.suppress_callback_exceptions = True
#https://www.pythonprogramming.in/create-document-term-matrix-with-tf-idf.html
