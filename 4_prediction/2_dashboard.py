# dashboard.py

import pandas as pd
import joblib
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# ============================
# 1. Cargar modelo y encoder
# ============================
model = joblib.load("rf_afore_model.pkl")
encoder = joblib.load("encoder_afore.pkl")

# Lista de AFOREs
afore_list = encoder.categories_[0]

# ============================
# 2. Crear app Dash
# ============================
app = Dash(__name__)
app.title = "Predicción de Rendimientos AFORE"

app.layout = html.Div([
    html.H1("Predicción de Rendimientos de AFOREs", style={'textAlign':'center'}),
    
    html.Div([
        html.Label("Selecciona el año para predecir:"),
        dcc.Input(id='input-year', type='number', value=2026, min=2000, max=2030, step=1)
    ], style={'width':'30%', 'padding':20}),
    
    html.Br(),
    
    html.Div(id='mensaje'),
    dcc.Graph(id='grafico-predicciones')
])

# ============================
# 3. Callback para actualizar predicciones
# ============================
@app.callback(
    Output('grafico-predicciones', 'figure'),
    Output('mensaje', 'children'),
    Input('input-year', 'value')
)
def update_dashboard(year_selected):
    if year_selected is None:
        return {}, "Por favor ingrese un año válido."
    
    # Crear dataframe para predicción
    future_df = pd.DataFrame({'año':[year_selected]*len(afore_list), 'afore':afore_list})
    
    # Codificar AFOREs
    afore_encoded = encoder.transform(future_df[['afore']])
    X_future = pd.concat([future_df[['año']], pd.DataFrame(afore_encoded, columns=encoder.get_feature_names_out(['afore']))], axis=1)
    
    # Predecir
    predicciones = model.predict(X_future)
    
    pred_df = pd.DataFrame({'AFORE': afore_list, 'Prediccion_Rendimiento': predicciones})
    pred_df = pred_df.sort_values(by='Prediccion_Rendimiento', ascending=False)
    
    # Mensaje resumen
    mejor = pred_df.iloc[0]
    mensaje = f"El AFORE con mayor rendimiento predicho en {year_selected} es {mejor['AFORE']} con {mejor['Prediccion_Rendimiento']:.2f}%"
    
    # Gráfico
    fig = px.bar(pred_df, x='Prediccion_Rendimiento', y='AFORE', orientation='h',
                 text='Prediccion_Rendimiento', color='Prediccion_Rendimiento',
                 color_continuous_scale='viridis', title=f"Predicción de rendimiento AFOREs para {year_selected}")
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    
    return fig, mensaje

# ============================
# 4. Ejecutar app
# ============================
if __name__ == '__main__':
    app.run(debug=True)
