from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Cargar datos
data = pd.read_csv('SP500_data_.csv')
data['Date'] = pd.to_datetime(data['Date'])  # Asegurar que la columna de fechas sea tipo datetime

# Inicializar app
app = Dash(__name__)

# Definir Layout
app.layout = html.Div([
    html.H2('Visualización de datos del S&P 500', style={'textAlign': 'center'}),

    html.Div([
        html.Label('Selecciona el tipo de dato:'),
        dcc.Dropdown(
            id='valor-dropdown',
            options=[
                {'label': 'Precio de Apertura', 'value': 'Open'},
                {'label': 'Precio de Cierre', 'value': 'Close'}
            ],
            value='Close',
            clearable=False
        ),

        html.Br(),

        html.Label('Elige un rango de fechas:'),
        dcc.DatePickerRange(
            id='rango-fechas',
            min_date_allowed=data['Date'].min(),
            max_date_allowed=data['Date'].max(),
            start_date=data['Date'].min(),
            end_date=data['Date'].max(),
            display_format='YYYY-MM-DD'
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),

    html.Div([
        dcc.Graph(id='grafico-lineal'),
        dcc.Graph(id='grafico-barras')
    ], style={'width': '65%', 'display': 'inline-block', 'padding': '20px'})
])

# Callback para actualizar los gráficos
@app.callback(
    Output('grafico-lineal', 'figure'),
    Output('grafico-barras', 'figure'),
    Input('valor-dropdown', 'value'),
    Input('rango-fechas', 'start_date'),
    Input('rango-fechas', 'end_date')
)
def actualizar_visualizaciones(tipo_valor, fecha_inicio, fecha_final):
    # Filtrar el dataframe
    mask = (data['Date'] >= fecha_inicio) & (data['Date'] <= fecha_final)
    datos_filtrados = data.loc[mask]

    if datos_filtrados.empty:
        fig_line = px.line(title="Sin datos disponibles para las fechas seleccionadas.")
        fig_bar = px.bar(title="Sin datos disponibles para las fechas seleccionadas.")
    else:
        # Gráfico de línea
        fig_line = px.line(
            datos_filtrados,
            x='Date',
            y=tipo_valor,
            title=f'Evolución de {tipo_valor} en el tiempo',
            markers=True
        )
        fig_line.update_traces(line_color='purple')

        # Gráfico de barras
        fig_bar = px.bar(
            datos_filtrados,
            x='Date',
            y='Volume',
            title='Volumen de transacciones por fecha'
        )
        fig_bar.update_traces(marker_color='orange')

    return fig_line, fig_bar

# Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)

