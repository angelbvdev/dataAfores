import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import joblib  

sns.set(style="whitegrid")

# ============================
# 1. Cargar dataset preparado
# ============================
df_anual = pd.read_csv("afore_anual.csv")

# ============================
# 2. Codificar variable AFORE
# ============================
encoder = OneHotEncoder(sparse_output=False)
afore_encoded = encoder.fit_transform(df_anual[['afore']])
df_afore_encoded = pd.DataFrame(afore_encoded, columns=encoder.get_feature_names_out(['afore']))

# Features y target
X = pd.concat([df_anual[['año']], df_afore_encoded], axis=1)
y = df_anual['rendimiento_anual']

# ============================
# 3. Dividir en entrenamiento y prueba
# ============================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ============================
# 4. Entrenar modelo Random Forest
# ============================
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluar modelo
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.4f}")

# ============================
# 5. Guardar modelo y encoder
# ============================
joblib.dump(model, "rf_afore_model.pkl")
joblib.dump(encoder, "encoder_afore.pkl")
print("Modelo y encoder guardados como 'rf_afore_model.pkl' y 'encoder_afore.pkl'")

# ============================
# 6. Predicción para un año futuro
# ============================
year_to_predict = int(input("Ingrese el año para predecir el mejor AFORE: "))

afore_list = encoder.categories_[0]
future_df = pd.DataFrame({'año': [year_to_predict]*len(afore_list),
                          'afore': afore_list})

# Codificar AFOREs
afore_future_encoded = encoder.transform(future_df[['afore']])
X_future = pd.concat([future_df[['año']], pd.DataFrame(afore_future_encoded, columns=encoder.get_feature_names_out(['afore']))], axis=1)

# Predicción
predicciones = model.predict(X_future)

# ============================
# 7. Resultados
# ============================
pred_df = pd.DataFrame({'AFORE': afore_list, 'Prediccion_Rendimiento': predicciones})
pred_df = pred_df.sort_values(by='Prediccion_Rendimiento', ascending=False)
print("\nPredicción de rendimientos para el año", year_to_predict)
print(pred_df)

# ============================
# 8. Visualización
# ============================
plt.figure(figsize=(10,6))
sns.barplot(data=pred_df, x='Prediccion_Rendimiento', y='AFORE', palette='viridis')
plt.title(f"Predicción de rendimiento de AFOREs para {year_to_predict}")
plt.xlabel("Rendimiento Predicho (%)")
plt.ylabel("AFORE")
plt.show()
