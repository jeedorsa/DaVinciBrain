# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import dash
from dash import dcc, html
from dash.dependencies import Output
from dash.dependencies import Input
from dash.dependencies import State
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

#Definir interfaz y funciones que se desean proporcionar al cliente.

#nterfaz con una entrada de archivo, un botón para cargar los datos y un gráfico para mostrar los datos cargados:
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Arrastra y suelta o ',
            html.A('selecciona archivos')
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
    html.Button('Cargar datos', id='load-data-button', n_clicks=0),
    dcc.Graph(id='data-graph')
])

# definir la lógica para cargar y mostrar los datos en el gráfico:

@app.callback(
    Output('data-graph', 'figure'),
    Input('load-data-button', 'n_clicks'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_graph(n_clicks, contents, filename):
    if n_clicks > 0 and contents is not None:
        # Leer los datos cargados en un DataFrame de pandas
        df = pd.read_csv(contents[0])
        # Generar un gráfico con Plotly Express
        fig = px.scatter(df, x='x', y='y')
        return fig
    else:
        # Si no se han cargado datos o no se ha hecho clic en el botón, retornar una figura vacía
        return {}

#Ejecucion
if __name__ == '__main__':
    app.run_server(debug=True)





