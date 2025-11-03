import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# ============================
# 1. Cargar dataset limpio
# ============================
df = pd.read_csv("../2_cleaning/afore_limpio.csv"   )
df['fecha'] = pd.to_datetime(df['fecha'])
df['año'] = df['fecha'].dt.year
df['mes'] = df['fecha'].dt.month

# ============================
# 2. Crear app Dash
# ============================
app = Dash(__name__)

# ============================
# 3. Layout de la app
# ============================
app.layout = html.Div([
    html.H1("Dashboard Rendimientos de AFORE", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Selecciona AFORE:"),
        dcc.Dropdown(
            options=[{'label': af, 'value': af} for af in df['afore'].unique()],
            value=df['afore'].unique()[0],
            id='afore-dropdown'
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'padding': 10}),
    
    html.Div([
        html.Label("Selecciona Plazo:"),
        dcc.Dropdown(
            options=[{'label': p, 'value': p} for p in df['plazo'].unique()],
            value=df['plazo'].unique()[0],
            id='plazo-dropdown'
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'padding': 10}),
    
    html.Br(),
    html.Div(id='mejor-peor-mes', style={'textAlign': 'center', 'fontSize': 18}),
    html.Br(),
    
    dcc.Graph(id='rendimiento-line'),
    dcc.Graph(id='rendimiento-hist'),
    dcc.Graph(id='rendimiento-anual'),
    dcc.Graph(id='volatilidad-anual'),
    dcc.Graph(id='heatmap-mes-año')
])

# ============================
# 4. Callbacks para interactividad
# ============================
@app.callback(
    Output('rendimiento-line', 'figure'),
    Output('rendimiento-hist', 'figure'),
    Output('rendimiento-anual', 'figure'),
    Output('volatilidad-anual', 'figure'),
    Output('heatmap-mes-año', 'figure'),
    Output('mejor-peor-mes', 'children'),
    Input('afore-dropdown', 'value'),
    Input('plazo-dropdown', 'value')
)
def update_dashboard(selected_afore, selected_plazo):
    # Filtrar datos
    filtered = df[(df['afore'] == selected_afore) & (df['plazo'] == selected_plazo)]
    
    # Mejor y peor mes
    mejor_mes = filtered.loc[filtered['rendimiento'].idxmax()]
    peor_mes = filtered.loc[filtered['rendimiento'].idxmin()]
    resumen = (f"Mejor mes: {mejor_mes['fecha'].strftime('%Y-%m')} con {mejor_mes['rendimiento']:.2f}% | "
               f"Peor mes: {peor_mes['fecha'].strftime('%Y-%m')} con {peor_mes['rendimiento']:.2f}%")
    
    # Gráfico de línea
    fig_line = px.line(
        filtered, x='fecha', y='rendimiento',
        title=f"Evolución del rendimiento: {selected_afore} ({selected_plazo})"
    )
    
    # Histograma + boxplot
    fig_hist = px.histogram(
        filtered, x='rendimiento', nbins=50, marginal='box',
        title=f"Distribución de rendimientos: {selected_afore} ({selected_plazo})"
    )
    
    # Rendimiento promedio anual
    promedio_anual = filtered.groupby('año')['rendimiento'].mean()
    fig_anual = px.bar(
        x=promedio_anual.index, y=promedio_anual.values,
        labels={'x':'Año','y':'Rendimiento (%)'},
        title=f"Rendimiento promedio anual: {selected_afore}"
    )
    
    # Volatilidad anual
    volatilidad_anual = filtered.groupby('año')['rendimiento'].std()
    fig_vol = px.bar(
        x=volatilidad_anual.index, y=volatilidad_anual.values,
        labels={'x':'Año','y':'Desviación estándar (%)'},
        title=f"Volatilidad anual: {selected_afore}"
    )
    
    # Heatmap por mes y año
    pivot = filtered.pivot_table(index='mes', columns='año', values='rendimiento', aggfunc='mean')
    fig_heat = px.imshow(
        pivot,
        labels=dict(x="Año", y="Mes", color="Rendimiento (%)"),
        x=pivot.columns,
        y=pivot.index,
        text_auto=".2f",
        aspect="auto",
        title=f"Rendimiento promedio por mes y año: {selected_afore}"
    )
    
    return fig_line, fig_hist, fig_anual, fig_vol, fig_heat, resumen

# ============================
# 5. Ejecutar app
# ============================
if __name__ == '__main__':
    app.run(debug=True)
