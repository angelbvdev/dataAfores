import pandas as pd

# ============================
# 1. Cargar dataset original
# ============================
df = pd.read_csv("../2_cleaning/afore_limpio.csv")

# ============================
# 2. Convertir fecha a datetime
# ============================
df['fecha'] = pd.to_datetime(df['fecha'])

# ============================
# 3. Crear columnas de año y mes
# ============================
df['año'] = df['fecha'].dt.year
df['mes'] = df['fecha'].dt.month


df_anual = df.groupby(['año', 'afore'])['rendimiento'].mean().reset_index()
df_anual.rename(columns={'rendimiento':'rendimiento_anual'}, inplace=True)

# ============================
# 5. Guardar dataset preparado
# ============================
df_anual.to_csv("afore_anual.csv", index=False)

print("Dataset preparado y guardado como 'afore_anual.csv'.")
print(df_anual.head())
