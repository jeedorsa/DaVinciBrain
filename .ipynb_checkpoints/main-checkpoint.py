import base64
import io
import dash
from dash import dcc, html
from dash.dependencies import Output, Input, State
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

# Definir el diseño y la lógica de tu aplicación Dash
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

# Definir la lógica para cargar y mostrar los datos en el gráfico
@app.callback(
    Output('data-graph', 'figure'),
    [Input('load-data-button', 'n_clicks')],
    [State('upload-data', 'contents'),
     State('upload-data', 'filename')]
)
def update_graph(n_clicks, contents, filename):
    if n_clicks > 0 and contents is not None:
        # Leer los datos cargados en un DataFrame de pandas
        content_type, content_string = contents[0].split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        # Generar gráficos con Plotly Express
        fig = px.histogram(df, x='x', nbins=10)
        fig.update_traces(opacity=0.75)  # Configurar la opacidad de las barras
        y=df['Egresado_Retirado'].value_counts() 
        fig.add_trace(px.line(df, x='Egresado_Retirado', y='y').data[0])  # Agregar la línea al gráfico
        
        return fig
    else:
        # Si no se han cargado datos o no se ha hecho clic en el botón, retornar una figura vacía
        return {}

# Ejecución
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
