import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

def create_dashboard(df):
    app = dash.Dash(__name__)
    
    fig = px.histogram(df, x="score", nbins=20, title="Distribution des scores de fiabilité")

    app.layout = html.Div([
        html.H1("Analyse des tweets"),
        dcc.Graph(figure=fig)
    ])

    return app

'''Affiche un histogramme interactif des scores de fiabilité.

Peut être intégré dans un dashboard web consultable par Thumalien.'''